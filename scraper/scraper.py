import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import json
import os

from .urls import BASE_URL, URLS


# -----------------------------
# Scrape a single page
# -----------------------------
async def scrape_page(page, url):
    print(f"Scraping: {url}")

    await page.goto(url, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_timeout(2000)

    content = await page.content()

    soup = BeautifulSoup(content, "html.parser")

    # Remove unwanted HTML tags
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    # Try to extract only the main content
    main = soup.find("main")

    if main:
        soup = main

    text = soup.get_text(separator="\n", strip=True)

    return {
        "url": url,
        "content": text
    }


# -----------------------------
# Remove duplicate paragraphs
# across all pages
# -----------------------------
def remove_global_duplicates(all_data):

    seen = set()

    cleaned_pages = []

    for page in all_data:

        paragraphs = page["content"].split("\n")

        unique = []

        for paragraph in paragraphs:

            paragraph = paragraph.strip()

            # Skip empty paragraphs
            if len(paragraph) < 10:
                continue

            # Skip duplicate paragraphs
            if paragraph in seen:
                continue

            seen.add(paragraph)

            unique.append(paragraph)

        page["content"] = "\n".join(unique)

        cleaned_pages.append(page)

    return cleaned_pages


# -----------------------------
# Main function
# -----------------------------
async def main():

    print(f"Starting scraper with {len(URLS)} URLs")

    all_data = []

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()

        for url in URLS:

            try:

                data = await scrape_page(page, url)

                # Skip pages with almost no content
                if len(data["content"]) > 100:
                    all_data.append(data)
                else:
                    print(f"Skipped {url} (Too little content)")

            except Exception as e:

                print(f"Failed {url}: {e}")

        await browser.close()

    # Remove duplicate paragraphs across pages
    all_data = remove_global_duplicates(all_data)

    # Create output folder
    os.makedirs("scraper/output", exist_ok=True)

    output_path = "scraper/output/website_content.json"

    with open(output_path, "w", encoding="utf-8") as f:

        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"\nTotal pages scraped : {len(all_data)}")
    print(f"File saved : {output_path}")


if __name__ == "__main__":
    asyncio.run(main())