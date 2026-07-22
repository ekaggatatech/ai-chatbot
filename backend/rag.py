import os
import chromadb
from sentence_transformers import SentenceTransformer
from.config import CHROMA_PATH,COLLECTION_NAME,EMBEDDING_MODEL,TOP_K

client=chromadb.PersistentClient(path=CHROMA_PATH)
try:
    collection=client.get_collection(COLLECTION_NAME)
except Exception:
    raise Exception(f"Collection '{COLLECTION_NAME} not found in {CHROMA_PATH}.Run your embedding first.")

embed_model=SentenceTransformer(EMBEDDING_MODEL)

def get_relevant_chunks(question:str):
    query_embedding=embed_model.encode(question).tolist()

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

if __name__ == "__main__":
    query = "What is hourmaker?"
    results = get_relevant_chunks(query)
    
    print("\n=== RAG RESULTS ===")
    if results:
        for i, r in enumerate(results, 1):
            print(f"\nResult {i}:")
            print(f"Text: {r['content']}")
            print(f"Source: {r['metadata']['url']}")
    else:
        print("No results found. Did you run loader.py first?")