import chromadb


client = chromadb.PersistentClient(
    path="./vector_db"
)


collection = client.get_or_create_collection(
    name="documents"
)



def store_document(doc_id, text):

    from ai.embedding import create_embedding


    embedding = create_embedding(text)


    collection.add(

        ids=[str(doc_id)],

        documents=[text],

        embeddings=[embedding],

        metadatas=[
            {
                "doc_id": str(doc_id)
            }
        ]

    )




def search_document(query, doc_id=None):

    from ai.embedding import create_embedding


    embedding = create_embedding(query)



    if doc_id:


        result = collection.query(

            query_embeddings=[embedding],

            n_results=3,

            where={
                "doc_id": str(doc_id)
            }

        )


    else:


        result = collection.query(

            query_embeddings=[embedding],

            n_results=3

        )



    return result["documents"]