import asyncio
import logging

import httpx

LOGGER = logging.getLogger(__name__)


class RhasspyError(Exception):
    pass


class RhasspyAPI:
    def __init__(self, url):
        transport = httpx.AsyncHTTPTransport(retries=7)  # tries for 30s
        timeout = httpx.Timeout(60)
        self.session = httpx.AsyncClient(transport=transport, timeout=timeout)
        self.session.headers.update(
            {"Content-Type": "application/json", "accept": "application/json"}
        )
        self.base_url = url

    async def get(self, url, *args, **kwargs):
        response = await self.session.get(f"{self.base_url}{url}", *args, **kwargs)
        if response.status_code == 500 and response.text:
            raise RhasspyError(response.text)
        response.raise_for_status()
        if response.headers["content-type"] == "application/json":
            return response.json()

    async def close(self):
        await self.session.aclose()
