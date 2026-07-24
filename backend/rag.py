import os
import chromadb
from sentence_transformers import SentenceTransformer
from.config import CHROMA_PATH,COLLECTION_NAME,EMBEDDING_MODEL,TOP_K
#Connect to the saved database folder
client=chromadb.PersistentClient(path=CHROMA_PATH)
#Try to open the data table, or show the error if it doesn't exist
try:
    collection=client.get_collection(COLLECTION_NAME)
except Exception:
    raise Exception(f"Collection '{COLLECTION_NAME} not found in {CHROMA_PATH}.Run your embedding first.")

embed_model=SentenceTransformer(EMBEDDING_MODEL)

def get_relevant_chunks(question:str):
    #It turn the user question into list 
    query_embedding=embed_model.encode(question).tolist()
    #Search the database for the top closest matches
    results=collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )

    docs=[]
    if results['documents'] and len(results['documents'][0])>0:
        for i in range(len(results['documents'][0])):
            docs.append({
                "content":results['documents'][0][i],
                "metadata":results['metadatas'][0][i] if results['metadatas'] else{}
            })
    return docs       