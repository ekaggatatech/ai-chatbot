import os
import asyncio
from urllib.parse import urlparse

from playwright.async_api import async_playwright
from .urls import URLS


SAVE_DIR = "scraper/output/html"

REMOVE_HIDDEN_JS = """
() => {
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

    const all = Array.from(document.querySelectorAll('body *'));
    all.forEach(el => {
        if (document.body.contains(el) && isHidden(el)) {
            el.remove();
        }
    });

    return document.body.innerHTML;
}
"""



def filename_from_url(url):
    """
    Convert URL into filename.
    """

    path = urlparse(url).path.strip("/")

    if path == "":
        return "home.html"

    return path.replace("/", "_") + ".html"


async def save_html(page, url):

    print(f"Scraping {url}")

    await page.goto(
        url,
        wait_until="networkidle",
        timeout=60000
    )

    # wait for React page
    await page.wait_for_timeout(3000)

    html = await page.evaluate(REMOVE_HIDDEN_JS)

    filename = filename_from_url(url)

    filepath = os.path.join(SAVE_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Saved -> {filename}")


async def main():

    os.makedirs(SAVE_DIR, exist_ok=True)

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)

        page = await browser.new_page()

        for url in URLS:
            try:
                await save_html(page, url)
            except Exception as e:
                print(f"Failed : {url}")
                print(e)

        await browser.close()

    print("\nFinished scraping all pages.")


if __name__ == "__main__":
    asyncio.run(main())