from sentence_transformers import SentenceTransformer
import json
model=SentenceTransformer("all-MiniLM-L6-v2")

def run_embedder():
    #open and read the previous generated text chunks
    with open("embedding/chunks.json","r", encoding="utf-8") as f :
        chunks=json.load(f)
    #Make the list containing only text from the chunks
    texts=[c["text"] for c in chunks]
    embeddings=model.encode(texts).tolist()
    
    #Put each list of numbers back into its matching text chunk
    for i , emb in enumerate(embeddings):
        chunks[i]["embedding"]=emb

    #Save everything into the same file
    with open("embedding/chunks.json","w",encoding="utf-8")as f:
        json.dump(chunks, f, ensure_ascii=False,indent=4)

    print(f"Added embeddings to{len(chunks)} chunks")

if __name__=="__main__":
    run_embedder()

