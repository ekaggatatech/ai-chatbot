import chromadb
from sentence_transformers import SentenceTransformer

model=SentenceTransformer("all-MiniLM-L6-v2")
client=chromadb.PersistentClient(path="embedding/chroma_db")
collection=client.get_collection(name="hourmaker_docs")

question=input("Test Search")

a_embedding=model.encode([question]).tolist()

results=collection.query(
    query_embeddings=a_embedding,
    n_results=3
)

print("\n---Top 3 result")
for i, doc in enumerate(results['documents'][0]):
    print(f"\n Result{i+1}")
    print(doc[:300]," ")
    print("URL:",results['metadatas'][0][i]['url'])