from sentence_transformers import SentenceTransformer
import json
model=SentenceTransformer("all-MiniLM-L6-v2")

def run_embedder():
    with open("embedding/chunks.json","r", encoding="utf-8") as f :
        chunks=json.load(f)

    texts=[c["text"] for c in chunks]
    embeddings=model.encode(texts).tolist()

    for i , emb in enumerate(embeddings):
        chunks[i]["embedding"]=emb

    with open("embedding/chunks.json","w",encoding="utf-8")as f:
        json.dump(chunks, f, ensure_ascii=False,indent=4)

    print(f"Added embeddings to{len(chunks)} chunks")

if __name__=="__main__":
    run_embedder()

