from fastapi import Body
from loguru import logger

from schemas import TextModelRequest
from scraper import extract_url,fetch_all

async def get_urls_content(body: TextModelRequest = Body(...)) -> str:
    urls=extract_url(body.prompt)
    if urls:
        try:
            urls_content=await fetch_all(urls)
            return urls_content
        except Exception as e:
            logger.warning(f"Error fetching content: {e}")
    return ""
    