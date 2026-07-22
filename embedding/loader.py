import json
import chromadb

def run_loader():
    with open("embedding/chunks.json","r",encoding="utf-8")as f:
        chunks=json.load(f)

    client=chromadb.PersistentClient(path="embedding/chroma_db")

    collection=client.get_or_create_collection(name="hourmaker_docs")

    ids=[c["id"] for c in chunks]
    documents=[c["text"] for c in chunks] 
    embeddings=[c["embedding"]for c in chunks] 
    metadatas=[{"url":c["url"]}for c in chunks]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )  

    print(f"Loaded{len(chunks)} chunks into ChromaDB")
    print(f"Databse saved at:embedding/chroma_db")

if __name__=="__main__":
    run_loader()    