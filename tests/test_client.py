import pytest
import httpx
import respx
from fastmcp.exceptions import ToolError
from fred_mcp.client import FredClient


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
            json={"error_code": 400, "error_message": "Bad Request. Variable series_id is not set."},
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
async def test_rate_limiter_tracks_requests(client):
    respx.get("https://api.stlouisfed.org/fred/series").mock(
        return_value=httpx.Response(200, json={"seriess": []})
    )
    for _ in range(5):
        await client.get("series", {"series_id": "GNPCA"})
    assert len(client._request_times) == 5
