import asyncio
import httpx
from bs4 import BeautifulSoup

base_url = 'https://arth-inacio.github.io/scod_scraping_challenge/'


async def buscar_page(client: httpx.AsyncClient, url: str) -> str | None:
    try:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.text
    except httpx.HTTPError as e:
        print(f"Erro ao acessar {url}: {e}")
        return None

    