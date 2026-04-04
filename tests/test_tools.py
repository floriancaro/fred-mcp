"""Smoke tests that exercise tools through the mounted FastMCP server."""

from __future__ import annotations

import httpx
import pytest
import respx

import fred_mcp.client
from fred_mcp.server import mcp


@pytest.fixture(autouse=True)
async def _reset_singleton(monkeypatch):
    """Ensure each test gets a fresh singleton client."""
    monkeypatch.setenv("FRED_API_KEY", "test-key-123")
    fred_mcp.client._client = None
    yield
    if fred_mcp.client._client is not None:
        await fred_mcp.client._client.close()
        fred_mcp.client._client = None


@respx.mock
@pytest.mark.asyncio
async def test_fred_series_tool():
    respx.get("https://api.stlouisfed.org/fred/series").mock(
        return_value=httpx.Response(200, json={"seriess": [{"id": "GNPCA"}]})
    )
    result = await mcp.call_tool("fred_series", arguments={"series_id": "GNPCA"})
    assert result.structured_content is not None
    assert result.structured_content.get("seriess")


@respx.mock
@pytest.mark.asyncio
async def test_fred_category_tool():
    respx.get("https://api.stlouisfed.org/fred/category").mock(
        return_value=httpx.Response(
            200, json={"categories": [{"id": 0, "name": "root"}]}
        )
    )
    result = await mcp.call_tool("fred_category", arguments={"category_id": 0})
    assert result.structured_content is not None
    assert result.structured_content.get("categories")


@respx.mock
@pytest.mark.asyncio
async def test_fred_releases_tool():
    respx.get("https://api.stlouisfed.org/fred/releases").mock(
        return_value=httpx.Response(200, json={"releases": []})
    )
    result = await mcp.call_tool("fred_releases", arguments={})
    assert result.structured_content is not None
    assert "releases" in result.structured_content


@respx.mock
@pytest.mark.asyncio
async def test_fred_sources_tool():
    respx.get("https://api.stlouisfed.org/fred/sources").mock(
        return_value=httpx.Response(200, json={"sources": []})
    )
    result = await mcp.call_tool("fred_sources", arguments={})
    assert result.structured_content is not None
    assert "sources" in result.structured_content


@respx.mock
@pytest.mark.asyncio
async def test_fred_tags_tool():
    respx.get("https://api.stlouisfed.org/fred/tags").mock(
        return_value=httpx.Response(200, json={"tags": []})
    )
    result = await mcp.call_tool("fred_tags", arguments={})
    assert result.structured_content is not None
    assert "tags" in result.structured_content
