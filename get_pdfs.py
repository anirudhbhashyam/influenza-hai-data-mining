import asyncio

from bs4 import BeautifulSoup

import httpx

import os

from pathlib import Path


common_headers: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


async def get_pdf_links(url) -> list[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers = common_headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")
        for link in links:
            pdf_links = [
                httpx.URL.join(url, link.get("href"))
                for link in links
                if link.get("href") and link.get("href").lower().endswith(".pdf")
            ]
    return pdf_links


async def download_pdf(url: httpx.URL, output_dir: Path):
    async with httpx.AsyncClient() as client:
        filename = os.path.join(output_dir, url.path.split("/")[-1])
        async with client.stream("GET", url, headers = common_headers) as response:
            response.raise_for_status()
            with open(filename, "wb") as f:
                async for chunk in response.aiter_bytes():
                    f.write(chunk)
    print(f"Downloaded: {filename}")


async def download_pdfs(urls: list[httpx.URL], output_dir: Path) -> None:
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            tg.create_task(
                download_pdf(url, output_dir)
            )


async def main() -> int:
    url = "https://www.crick.ac.uk/research/platforms-and-facilities/worldwide-influenza-centre/annual-and-interim-reports"
    pdf_links = await get_pdf_links(url)
    out_dir = Path("pdf_data").resolve()
    print(f"Found {len(pdf_links)} PDFs.")
    await download_pdfs(pdf_links, out_dir)
    return 0
    

if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))