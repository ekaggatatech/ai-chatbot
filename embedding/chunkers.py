import json
def chunk(text, chunk_size=500,overlap=50):
    words=text.split()
    chunks=[]
    for i in range(0,len(words),chunk_size-overlap):
        chunk=" ".join(words[i:i+chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks
        
def run_chunker():
    with open("scraper/output/website_content.json", "r", encoding="utf-8") as f:
        pages = json.load(f)
        
        
        all_chunks = []
        for page in pages:
            chunks = chunk(page["content"])
            for i, chunk_text in enumerate(chunks):
                all_chunks.append({
                    "id": f"{page['url']}#chunk{i}",
                    "url": page["url"],
                    "text": chunk_text  
                })
            
    with open("embedding/chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=4)
        
    print(f"Created {len(all_chunks)} chunks in embedding/chunks.json")


if __name__=="__main__":
    run_chunker()