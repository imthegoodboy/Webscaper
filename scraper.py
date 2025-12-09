import re
import asyncio

import aiohttp
from bs4 import BeautifulSoup
from loguru import logger

def extract_url(text:str)->lisr[str]:
    url_pattern=r"(?P<url>https?://[^\s]+)"
    urls=re.findall(url_pattern,text)
    return urls


def parse_inner_text(html_string:str)->str:
    soup=BeautifulSoup(html_string,"lxml")
    if content:=soup.find("div",id="bodyContent"):
        return content.get_text()

    logger.error("No content found in the HTML string")
    return ""

async def fetch(session:aiohttp.ClientSession,url:str)->str:
    async with session.get(url) as response:
        html_string=await response.text()
        return parse_inner_text(html_string)


async def fetch_all(urls:list[str])->list[str]:
    async with aiohttp.ClientSession() as session:
        results=await asyncio.gather(*[fetch(session,url) for url in urls],return_exceptions=True)
    success_results = [result for result in results if isinstance(result, str)]

    if len(results)!=len(success_results):
        logger.warning(f"Failed to fetch {len(results)-len(success_results)} URLs")
    return " ".join(success_results)