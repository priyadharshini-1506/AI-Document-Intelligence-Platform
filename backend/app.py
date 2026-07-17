from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

from services.docx_reader import read_docx
from services.pdf_reader import read_pdf
from services.image_reader import read_image


from ai.groq_service import (
    summarize_document,
    classify_document,
    answer_question
)

from ai.extractor import extract_information


from database.database import (
    engine,
    Base,
    SessionLocal
)

from database import models


from vector_db.vector_store import (
    store_document,
    search_document
)


from datetime import datetime

import os
import shutil



# -----------------------------------
# Create Database
# -----------------------------------

Base.metadata.create_all(
    bind=engine
)



app = FastAPI()



UPLOAD_FOLDER = "uploads"


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)





# -----------------------------------
# File Organization
# -----------------------------------

def organize_file(
        filepath,
        document_type
):


    folder_mapping = {

        "Resume":"Resume",

        "Invoice":"Invoice",

        "Medical Report":"Medical_Report",

        "Research Paper":"Research_Paper",

        "Legal Contract":"Legal_Contract",

        "Letter":"Letter",

        "Certificate":"Certificate",

        "Other":"Other"

    }



    folder_name = folder_mapping.get(

        document_type,

        "Other"

    )



    destination_folder = os.path.join(

        UPLOAD_FOLDER,

        folder_name

    )



    os.makedirs(

        destination_folder,

        exist_ok=True

    )



    destination_path = os.path.join(

        destination_folder,

        os.path.basename(filepath)

    )



    shutil.move(

        filepath,

        destination_path

    )


    return destination_path







# -----------------------------------
# Home
# -----------------------------------

@app.get("/")
def home():

    return {

        "message":
        "Welcome to AI Document Automation System"

    }









# -----------------------------------
# Upload Document
# -----------------------------------

@app.post("/upload")
async def upload_document(
        file: UploadFile = File(...)
):


    allowed_extensions=[

        ".pdf",
        ".docx",
        ".jpg",
        ".jpeg",
        ".png"

    ]



    extension=os.path.splitext(

        file.filename

    )[1].lower()



    if extension not in allowed_extensions:


        return {

            "error":
            "Unsupported file type"

        }





    # Save file temporarily

    filepath=os.path.join(

        UPLOAD_FOLDER,

        file.filename

    )



    with open(filepath,"wb") as buffer:


        shutil.copyfileobj(

            file.file,

            buffer

        )







    # -----------------------------------
    # Text Extraction
    # -----------------------------------

    document_text=""



    if extension == ".docx":


        document_text = read_docx(

            filepath

        )



    elif extension == ".pdf":


        document_text = read_pdf(

            filepath

        )



    elif extension in [

        ".jpg",
        ".jpeg",
        ".png"

    ]:


        document_text = read_image(

            filepath

        )








    # -----------------------------------
    # AI Processing
    # -----------------------------------

    summary=""

    document_type="Other"

    extracted_information={}




    if document_text.strip():



        summary = summarize_document(

            document_text

        )



        document_type = classify_document(

            document_text

        )



        # Step 21

        extracted_information = extract_information(

            document_text,

            document_type

        )









    # -----------------------------------
    # Move File
    # -----------------------------------

    organized_path = organize_file(

        filepath,

        document_type

    )









    # -----------------------------------
    # Save SQLite
    # -----------------------------------

    db = SessionLocal()



    new_document = models.Document(


        filename=file.filename,


        document_type=document_type,


        summary=summary,


        file_path=organized_path,


        uploaded_time=str(datetime.now())


    )



    db.add(new_document)


    db.commit()


    db.refresh(new_document)







    # -----------------------------------
    # Store Vector Database
    # -----------------------------------

    if document_text.strip():


        store_document(

            new_document.id,

            document_text

        )



    db.close()







    return {


        "filename":
        file.filename,


        "message":
        "File uploaded successfully",



        "document_id":
        new_document.id,



        "document_type":
        document_type,



        "saved_to":
        organized_path,



        "summary":
        summary,



        "extracted_information":
        extracted_information,



        "vector_status":
        "Stored in ChromaDB"

    }









# -----------------------------------
# Document History
# -----------------------------------

@app.get("/documents")
def get_documents():


    db = SessionLocal()



    documents = db.query(

        models.Document

    ).all()



    result=[]



    for doc in documents:


        result.append({

            "id":
            doc.id,


            "filename":
            doc.filename,


            "type":
            doc.document_type,


            "uploaded_time":
            doc.uploaded_time

        })



    db.close()



    return result











# -----------------------------------
# Chat With Document
# -----------------------------------

@app.post("/search")
def search_documents(

        question:str,

        doc_id:int

):


    results = search_document(

        question,

        doc_id

    )



    if not results or not results[0]:


        return {

            "answer":
            "No information found."

        }





    context="\n".join(

        results[0]

    )




    answer = answer_question(

        context,

        question

    )




    return {


        "question":
        question,


        "answer":
        answer

    }









# -----------------------------------
# Preview Document
# -----------------------------------

@app.get("/preview/{doc_id}")
def preview_document(

        doc_id:int

):


    db=SessionLocal()



    document=db.query(

        models.Document

    ).filter(

        models.Document.id == doc_id

    ).first()



    db.close()



    if not document:


        return {

            "error":
            "Document not found"

        }




    return FileResponse(

        path=document.file_path

    )









# -----------------------------------
# Download Document
# -----------------------------------

@app.get("/download/{doc_id}")
def download_document(

        doc_id:int

):


    db=SessionLocal()



    document=db.query(

        models.Document

    ).filter(

        models.Document.id == doc_id

    ).first()



    db.close()



    if not document:


        return {

            "error":
            "Document not found"

        }




    return FileResponse(

        path=document.file_path,

        filename=document.filename

    )









# -----------------------------------
# Delete Document
# -----------------------------------

@app.delete("/delete/{doc_id}")
def delete_document(

        doc_id:int

):


    db=SessionLocal()



    document=db.query(

        models.Document

    ).filter(

        models.Document.id == doc_id

    ).first()



    if not document:


        db.close()


        return {

            "error":
            "Document not found"

        }







    if os.path.exists(

        document.file_path

    ):


        os.remove(

            document.file_path

        )






    db.delete(document)


    db.commit()


    db.close()



    return {


        "message":
        "Document deleted successfully"

    }