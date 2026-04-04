import httpx
import pytest
import respx
from fastmcp.exceptions import ToolError

import fred_mcp.client
from fred_mcp.client import FredClient, get_client


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setenv("FRED_API_KEY", "test-key-123")
    return FredClient()


@respx.mock
@pytest.mark.asyncio
async def test_get_injects_api_key_and_file_type(client):
    route = respx.get("https://api.stlouisfed.org/fred/series").mock(
        return_value=httpx.Response(200, json={"seriess": []})
    )
    result = await client.get("series", {"series_id": "GNPCA"})
    assert route.called
    request = route.calls[0].request
    assert "api_key=test-key-123" in str(request.url)
    assert "file_type=json" in str(request.url)
    assert "series_id=GNPCA" in str(request.url)
    assert result == {"seriess": []}


@respx.mock
@pytest.mark.asyncio
async def test_get_strips_none_params(client):
    route = respx.get("https://api.stlouisfed.org/fred/series").mock(
        return_value=httpx.Response(200, json={"seriess": []})
    )
    await client.get("series", {"series_id": "GNPCA", "limit": None, "offset": None})
    request = route.calls[0].request
    url_str = str(request.url)
    assert "limit" not in url_str
    assert "offset" not in url_str
    assert "series_id=GNPCA" in url_str


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.delenv("FRED_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="FRED_API_KEY"):
        FredClient()


@respx.mock
@pytest.mark.asyncio
async def test_fred_api_error_raised(client):
    respx.get("https://api.stlouisfed.org/fred/series").mock(
        return_value=httpx.Response(
            200,
            json={
                "error_code": 400,
                "error_message": "Bad Request. Variable series_id is not set.",
            },
        )
    )
    with pytest.raises(ToolError, match="Bad Request"):
        await client.get("series", {})


@respx.mock
@pytest.mark.asyncio
async def test_http_error_raised(client):
    respx.get("https://api.stlouisfed.org/fred/series").mock(
        return_value=httpx.Response(500, text="Internal Server Error")
    )
    with pytest.raises(ToolError, match="HTTP 500"):
        await client.get("series", {"series_id": "GNPCA"})


@respx.mock
@pytest.mark.asyncio
async def test_fred_api_error_without_message(client):
    respx.get("https://api.stlouisfed.org/fred/series").mock(
        return_value=httpx.Response(200, json={"error_code": 500})
    )
    with pytest.raises(ToolError, match="Unknown error"):
        await client.get("series", {})


@respx.mock
@pytest.mark.asyncio
async def test_network_error_raised(client):
    respx.get("https://api.stlouisfed.org/fred/series").mock(
        side_effect=httpx.ConnectError("Connection refused")
    )
    with pytest.raises(ToolError, match="Failed to connect"):
        await client.get("series", {"series_id": "GNPCA"})


@respx.mock
@pytest.mark.asyncio
async def test_invalid_json_raised(client):
    respx.get("https://api.stlouisfed.org/fred/series").mock(
        return_value=httpx.Response(200, text="not json at all")
    )
    with pytest.raises(ToolError, match="invalid JSON"):
        await client.get("series", {"series_id": "GNPCA"})


@pytest.mark.asyncio
async def test_get_client_returns_singleton(monkeypatch):
    monkeypatch.setenv("FRED_API_KEY", "test-key-123")
    fred_mcp.client._client = None
    try:
        a = await get_client()
        b = await get_client()
        assert a is b
    finally:
        await fred_mcp.client.reset_client()


@pytest.mark.asyncio
async def test_reset_client_closes_and_clears(monkeypatch):
    monkeypatch.setenv("FRED_API_KEY", "test-key-123")
    fred_mcp.client._client = None
    # Create a client via get_client
    client = await get_client()
    assert fred_mcp.client._client is client
    # Reset should close and clear
    await fred_mcp.client.reset_client()
    assert fred_mcp.client._client is None


@pytest.mark.asyncio
async def test_reset_client_noop_when_none(monkeypatch):
    monkeypatch.setenv("FRED_API_KEY", "test-key-123")
    fred_mcp.client._client = None
    # Should not raise when no client exists
    await fred_mcp.client.reset_client()
    assert fred_mcp.client._client is None


@respx.mock
@pytest.mark.asyncio
async def test_rate_limiter_tracks_requests(client):
    respx.get("https://api.stlouisfed.org/fred/series").mock(
        return_value=httpx.Response(200, json={"seriess": []})
    )
    for _ in range(5):
        await client.get("series", {"series_id": "GNPCA"})
    assert len(client._request_times) == 5


@respx.mock
@pytest.mark.asyncio
async def test_get_with_base_url_override(client):
    route = respx.get("https://api.stlouisfed.org/geofred/series/group").mock(
        return_value=httpx.Response(200, json={"series_group": []})
    )
    result = await client.get("series/group", base_url="https://api.stlouisfed.org/geofred/")
    assert route.called
    request = route.calls[0].request
    assert "api_key=test-key-123" in str(request.url)
    assert "file_type=json" in str(request.url)
    assert result == {"series_group": []}


@respx.mock
@pytest.mark.asyncio
async def test_http_4xx_includes_fred_error_message(client):
    respx.get("https://api.stlouisfed.org/fred/series").mock(
        return_value=httpx.Response(
            400,
            json={"error_message": "Bad Request. Variable series_id is not set."},
        )
    )
    with pytest.raises(ToolError, match="Variable series_id is not set"):
        await client.get("series", {})


@respx.mock
@pytest.mark.asyncio
async def test_http_4xx_without_json_body(client):
    respx.get("https://api.stlouisfed.org/fred/series").mock(
        return_value=httpx.Response(400, text="Bad Request")
    )
    with pytest.raises(ToolError, match="HTTP 400"):
        await client.get("series", {})


@respx.mock
@pytest.mark.asyncio
async def test_get_with_base_url_no_trailing_slash(client):
    route = respx.get("https://api.stlouisfed.org/geofred/series/group").mock(
        return_value=httpx.Response(200, json={"series_group": []})
    )
    result = await client.get("series/group", base_url="https://api.stlouisfed.org/geofred")
    assert route.called
    assert result == {"series_group": []}


@respx.mock
@pytest.mark.asyncio
async def test_timeout_error_raised(client):
    respx.get("https://api.stlouisfed.org/fred/series").mock(
        side_effect=httpx.ReadTimeout("Read timed out")
    )
    with pytest.raises(ToolError, match="timed out"):
        await client.get("series", {"series_id": "GNPCA"})
