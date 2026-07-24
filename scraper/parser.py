import os
import json
from bs4 import BeautifulSoup
HTML_DIR = "scraper/output/html"
OUTPUT_FILE = "scraper/output/website_content.json"


def clean_text(text):
    # Remove extra spaces and blank lines.
    if not text:
        return ""

    lines = []
    #Split the text into line and skip empty lines
    for line in text.splitlines():
        line=line.strip()
        if line:
            lines.append(line)

    return "\n".join(lines)        



def is_excluded_feature(tag):
    classes = tag.get("class", [])
    return "text-muted-foreground" in classes

def is_leaf_div(tag):
    if tag.name!="div":
        return True
    return not tag.find(["h1","h2","h3","li","p","div"])


def parse_html(filepath):

    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted tags
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    main = soup.find("main")

    if main:
        soup = main

    page_sections = []

    current_section = None

    for element in soup.find_all([
        "h1",
        "h2",
        "h3",
        "p",
        "li",
        "div"
    ]):

        if element.name=="div" and not is_leaf_div(element):
            continue

        # New section starts
        if element.name in ["h1", "h2", "h3"]:

            if current_section:
                page_sections.append(current_section)

            current_section = {
                "heading": clean_text(element.get_text(" ", strip=True)),
                "content": []
            }

        else:

            text = clean_text(element.get_text(" ", strip=True))

            if not text:
                continue

            # Mark excluded pricing features instead of listing them as included
            if element.name == "li" and is_excluded_feature(element):
                text = f"{text} (not included)"

            if current_section is None:
                current_section = {
                    "heading": "General",
                    "content": []
                }

            current_section["content"].append(text)

    if current_section:
        page_sections.append(current_section)

    return page_sections


def run_parser():

    pages = []

    for filename in sorted(os.listdir(HTML_DIR)):

        if not filename.endswith(".html"):
            continue

        filepath = os.path.join(HTML_DIR, filename)

        print(f"Parsing {filename}")

        sections = parse_html(filepath)

        pages.append({
            "page": filename.replace(".html", ""),
            "sections": sections
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            pages,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nSaved {len(pages)} pages.")
    print(f"Output -> {OUTPUT_FILE}")


if __name__ == "__main__":
    run_parser()