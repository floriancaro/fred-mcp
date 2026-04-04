from __future__ import annotations

import asyncio
import os
import time
from collections import deque

import httpx
from fastmcp.exceptions import ToolError

BASE_URL = "https://api.stlouisfed.org/fred/"
RATE_LIMIT = 120
RATE_WINDOW = 60  # seconds


class FredClient:
    def __init__(self) -> None:
        api_key = os.environ.get("FRED_API_KEY")
        if not api_key:
            raise RuntimeError(
                "FRED_API_KEY environment variable is not set. "
                "Get a free API key at https://fred.stlouisfed.org/docs/api/api_key.html"
            )
        self._api_key = api_key
        self._http = httpx.AsyncClient(base_url=BASE_URL, timeout=30.0)
        self._request_times: deque[float] = deque()
        self._rate_lock = asyncio.Lock()

    async def _rate_limit(self) -> None:
        async with self._rate_lock:
            now = time.monotonic()
            while self._request_times and now - self._request_times[0] > RATE_WINDOW:
                self._request_times.popleft()
            if len(self._request_times) >= RATE_LIMIT:
                sleep_time = RATE_WINDOW - (now - self._request_times[0])
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
            self._request_times.append(time.monotonic())

    async def get(self, endpoint: str, params: dict | None = None) -> dict:
        await self._rate_limit()
        request_params = {k: v for k, v in (params or {}).items() if v is not None}
        request_params["api_key"] = self._api_key
        request_params["file_type"] = "json"
        try:
            response = await self._http.get(endpoint, params=request_params)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise ToolError(
                f"FRED API returned HTTP {e.response.status_code} for {endpoint}. "
                "The server may be temporarily unavailable — try again shortly."
            ) from e
        except httpx.RequestError as e:
            raise ToolError(f"Failed to connect to FRED API: {e}") from e
        try:
            data = response.json()
        except ValueError as e:
            raise ToolError(f"FRED API returned invalid JSON for {endpoint}") from e
        if "error_code" in data:
            raise ToolError(
                f"FRED API error: {data.get('error_message', 'Unknown error')}"
            )
        return data

    async def close(self) -> None:
        await self._http.aclose()


_client: FredClient | None = None
_client_lock = asyncio.Lock()


async def get_client() -> FredClient:
    global _client
    if _client is None:
        async with _client_lock:
            if _client is None:
                _client = FredClient()
    return _client
