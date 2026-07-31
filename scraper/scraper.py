import os
import asyncio
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from .urls import URLS

#It's a directory where the scraped html file saved
SAVE_DIR = "scraper/output/html"

REMOVE_HIDDEN_JS = """
() => {
//It is a helper function to check if the element is hidden from view
    const isHidden = (el) => {
        const style = window.getComputedStyle(el);
        if (style.display === 'none') return true;
        if (style.visibility === 'hidden') return true;
        if (parseFloat(style.opacity) === 0) return true;
        if (el.hasAttribute('hidden')) return true;
        if (el.getAttribute('aria-hidden') === 'true') return true;

        const rect = el.getBoundingClientRect();
        if (rect.width === 0 && rect.height === 0) return true;

        return false;
    };

    //It select the element inside the body tag
    const all = Array.from(document.querySelectorAll('body *'));
    //It loop through the elements and remove which is hidden
    all.forEach(el => {
        if (document.body.contains(el) && isHidden(el)) {
            el.remove();
        }
    });
    //Return the clean inner html string of the body
    return document.body.innerHTML;
}
"""
def filename_from_url(url):
    
    # Convert URL into filename.

    path = urlparse(url).path.strip("/")

    if path == "":
        return "home.html"

    return path.replace("/", "_") + ".html"


async def save_html(page, url):
    # navigate to a url , clean the hidden elements and save the content

    print(f"Scraping {url}")

    #it navigate the url and wait for the network activity to stop
    await page.goto(
        url,
        wait_until="networkidle",
        timeout=60000
    )

    # wait for React page
    await page.wait_for_timeout(3000)

    html = await page.evaluate(REMOVE_HIDDEN_JS)

    filename = filename_from_url(url)

    #Generate the save path and write the output file
    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Saved -> {filename}")


async def main():
    #Create a output directory if it doesn't exist already
    os.makedirs(SAVE_DIR, exist_ok=True)

    async with async_playwright() as p:
        #Launch a headless chromium browser instance
        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()
        #Iterate and Scrape the every url 
        for url in URLS:
            try:
                await save_html(page, url)
            except Exception as e:
                #Catch any network or rendering the error to prevent crash
                print(f"Failed : {url}")
                print(e)

        await browser.close()

    print("\nFinished scraping all pages.")


if __name__ == "__main__":
    asyncio.run(main())