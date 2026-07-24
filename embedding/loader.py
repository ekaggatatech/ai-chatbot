import json
import os
import chromadb


def run_loader():

    with open("embedding/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    #Create a database folder if it not exist
    os.makedirs("embedding/chroma_db", exist_ok=True)
    #Connect to ChromaDB and tell it where to save the data on the computer
    client = chromadb.PersistentClient(path="embedding/chroma_db")
    #Get or Create the a storage table which called collection with name.
    collection = client.get_or_create_collection(name="hourmaker_docs")
    #Extract the id,text and metadata
    ids = [c["id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [
        {
            "url": c["url"],
            "page_title": c["page_title"],
            "section_title": c["section_title"]
        }
        for c in chunks
    ]
    embeddings=[c["embedding"] for c in chunks]
    #It upload all the prepared pieces into the database collection.
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"Loaded {len(chunks)} chunks into ChromaDB")
    print(f"Database is saved :embedding/chroma_db")


if __name__ == "__main__":
    run_loader()