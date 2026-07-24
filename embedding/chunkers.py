import json

def split_large_section(text,chunk_size=100,overlap=20):
    #Split a large block of text into smaller overlapping chunks based on word count.
    #This creates sliding windows of text to preserve context across splits.
    words=text.split()
    chunks=[]
    step=chunk_size-overlap
    #Using the loop to the list of words using the step interval
    for i in range(0, len(words), step):
    #Extract the slice of words and join them back to a string
        chunk = " ".join(words[i:i + chunk_size])

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def run_chunker():

    with open("scraper/output/website_content.json", "r", encoding="utf-8") as f:
        #It load the parse , structured website content to JSON file
        pages = json.load(f)

    all_chunks = []
    #It iterate each page in sequence.
    for page in pages:

        page_url = page["page"]
        page_title = page["page"]

        sections = page["sections"]

        section_counters = {}

        for section in sections:

            section_title = section["heading"]

            section_content = f"{section_title}. " + " ".join(section["content"]).strip()

            # Skip if there is nothing but the heading only
            if section_content.strip() == f"{section_title}.":
                continue

            key = f"{page_url}#{section_title}"
            section_counters[key] = section_counters.get(key, -1) + 1
            occurrence = section_counters[key]

            base_id = key if occurrence == 0 else f"{key}_dup{occurrence}"

            if len(section_content.split()) <= 100:

                all_chunks.append(
                    {
                        "id": base_id,
                        "url": page_url,
                        "page_title": page_title,
                        "section_title": section_title,
                        "text": section_content
                    }
                )

            else:
            # Split large content text into multiple sub-chunks 
                chunks = split_large_section(section_content)
                #Store the snmaller chunks with an indexed and id
                for i, chunk in enumerate(chunks):

                    all_chunks.append(
                        {
                            "id": f"{base_id}_{i}",
                            "url": page_url,
                            "page_title": page_title,
                            "section_title": section_title,
                            "text": chunk
                        }
                    )
    #Save it into the file chunks.json 
    with open("embedding/chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=4)

    print(f"Created {len(all_chunks)} chunks")


if __name__ == "__main__":
    run_chunker()