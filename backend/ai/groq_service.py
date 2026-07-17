import os
from dotenv import load_dotenv
from groq import Groq


# Load API key
load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)



# --------------------------------
# AI Summary
# --------------------------------

def summarize_document(text):

    prompt = f"""

    Summarize the following document in 5 bullet points.

    Document:

    {text}

    """


    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],

        temperature=0.3

    )


    return response.choices[0].message.content





# --------------------------------
# AI Document Classification
# --------------------------------

def classify_document(text):


    prompt = f"""

    You are an AI document classifier.

    Classify the document into ONLY ONE category.

    Categories:

    - Resume
    - Invoice
    - Medical Report
    - Research Paper
    - Legal Contract
    - Letter
    - Certificate
    - Other


    Return ONLY category name.


    Document:

    {text}

    """



    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role":"user",
                "content":prompt
            }

        ],

        temperature=0

    )



    return response.choices[0].message.content.strip()






# --------------------------------
# AI Question Answering (RAG)
# --------------------------------


def answer_question(context, question):


    prompt = f"""

    You are an AI document assistant.

    Answer the question using ONLY the provided document information.


    Document Information:

    {context}


    User Question:

    {question}


    Give a simple and accurate answer.

    """



    response = client.chat.completions.create(


        model="llama-3.3-70b-versatile",


        messages=[

            {
                "role":"user",
                "content":prompt
            }

        ],


        temperature=0.2

    )



    return response.choices[0].message.content