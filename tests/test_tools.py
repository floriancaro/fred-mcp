"""Comprehensive parametrized test suite for all 33 FRED MCP tools."""

from __future__ import annotations

import httpx
import pytest
import respx
from fastmcp.exceptions import ToolError

import fred_mcp.client
from fred_mcp.server import mcp

# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
async def _reset_singleton(monkeypatch):
    """Ensure each test gets a fresh singleton client."""
    monkeypatch.setenv("FRED_API_KEY", "test-key-123")
    fred_mcp.client._client = None
    yield
    if fred_mcp.client._client is not None:
        await fred_mcp.client._client.close()
        fred_mcp.client._client = None


# ---------------------------------------------------------------------------
# Test 1: smoke test all 29 tools
# ---------------------------------------------------------------------------

TOOL_CASES = [
    # series (10)
    ("fred_series", "series", {"series_id": "GNPCA"}, "seriess"),
    ("fred_series_search", "series/search", {"search_text": "gdp"}, "seriess"),
    ("fred_series_observations", "series/observations", {"series_id": "GNPCA"}, "observations"),
    ("fred_series_categories", "series/categories", {"series_id": "GNPCA"}, "categories"),
    ("fred_series_release", "series/release", {"series_id": "GNPCA"}, "releases"),
    ("fred_series_tags", "series/tags", {"series_id": "GNPCA"}, "tags"),
    ("fred_series_search_tags", "series/search/tags", {"series_search_text": "gdp"}, "tags"),
    (
        "fred_series_search_related_tags",
        "series/search/related_tags",
        {"series_search_text": "gdp", "tag_names": "usa"},
        "tags",
    ),
    ("fred_series_updates", "series/updates", {}, "seriess"),
    ("fred_series_vintagedates", "series/vintagedates", {"series_id": "GNPCA"}, "vintage_dates"),
    # categories (5)
    ("fred_category", "category", {"category_id": 0}, "categories"),
    ("fred_category_children", "category/children", {"category_id": 0}, "categories"),
    ("fred_category_related", "category/related", {"category_id": 32073}, "categories"),
    ("fred_category_series", "category/series", {"category_id": 125}, "seriess"),
    ("fred_category_tags", "category/tags", {"category_id": 125}, "tags"),
    # releases (8)
    ("fred_releases", "releases", {}, "releases"),
    ("fred_releases_dates", "releases/dates", {}, "release_dates"),
    ("fred_release", "release", {"release_id": 53}, "releases"),
    ("fred_release_dates", "release/dates", {"release_id": 53}, "release_dates"),
    ("fred_release_series", "release/series", {"release_id": 53}, "seriess"),
    ("fred_release_sources", "release/sources", {"release_id": 53}, "sources"),
    ("fred_release_tags", "release/tags", {"release_id": 53}, "tags"),
    ("fred_release_tables", "release/tables", {"release_id": 53}, "elements"),
    # sources (3)
    ("fred_sources", "sources", {}, "sources"),
    ("fred_source", "source", {"source_id": 1}, "sources"),
    ("fred_source_releases", "source/releases", {"source_id": 1}, "releases"),
    # tags (3)
    ("fred_tags", "tags", {}, "tags"),
    ("fred_related_tags", "related_tags", {"tag_names": "monetary aggregates"}, "tags"),
    ("fred_tags_series", "tags/series", {"tag_names": "slovenia"}, "seriess"),
    # geo (4)
    (
        "geofred_series_group",
        "https://api.stlouisfed.org/geofred/series/group",
        {"series_id": "SMU56000000500000001a"},
        "series_group",
    ),
    (
        "geofred_series_data",
        "https://api.stlouisfed.org/geofred/series/data",
        {"series_id": "WIPCPI"},
        "meta",
    ),
    (
        "geofred_regional_data",
        "https://api.stlouisfed.org/geofred/regional/data",
        {
            "series_group": "882",
            "region_type": "state",
            "date": "2013-01-01",
            "season": "NSA",
            "units": "Dollars",
        },
        "meta",
    ),
    (
        "geofred_shapes",
        "https://api.stlouisfed.org/geofred/shapes/file",
        {"shape": "state"},
        "type",
    ),
]


@respx.mock
@pytest.mark.asyncio
@pytest.mark.parametrize("tool_name,endpoint,args,response_key", TOOL_CASES)
async def test_tool_call(tool_name, endpoint, args, response_key):
    url = (
        endpoint
        if endpoint.startswith("https://")
        else f"https://api.stlouisfed.org/fred/{endpoint}"
    )
    respx.get(url).mock(return_value=httpx.Response(200, json={response_key: []}))
    result = await mcp.call_tool(tool_name, arguments=args)
    assert result.structured_content is not None
    assert response_key in result.structured_content


# ---------------------------------------------------------------------------
# Test 2: verify args reach the HTTP request
# ---------------------------------------------------------------------------

PARAM_FLOW_CASES = [
    ("fred_series", "series", {"series_id": "GNPCA"}, {"series_id": "GNPCA"}),
    ("fred_release", "release", {"release_id": 53}, {"release_id": "53"}),
    (
        "fred_series_search",
        "series/search",
        {"search_text": "gdp", "limit": 10},
        {"search_text": "gdp", "limit": "10"},
    ),
    (
        "fred_series_observations",
        "series/observations",
        {"series_id": "GNPCA", "units": "pch", "frequency": "m"},
        {"series_id": "GNPCA", "units": "pch", "frequency": "m"},
    ),
    (
        "geofred_regional_data",
        "https://api.stlouisfed.org/geofred/regional/data",
        {
            "series_group": "882",
            "region_type": "state",
            "date": "2013-01-01",
            "season": "NSA",
            "units": "Dollars",
            "frequency": "a",
            "transformation": "lin",
            "aggregation_method": "avg",
        },
        {
            "series_group": "882",
            "region_type": "state",
            "date": "2013-01-01",
            "season": "NSA",
            "units": "Dollars",
            "frequency": "a",
            "transformation": "lin",
            "aggregation_method": "avg",
        },
    ),
]


@respx.mock
@pytest.mark.asyncio
@pytest.mark.parametrize("tool_name,endpoint,args,expected_params", PARAM_FLOW_CASES)
async def test_params_flow_to_request(tool_name, endpoint, args, expected_params):
    # Capture the request by keying the response key from tool cases lookup
    response_key = next(rc for tc, ep, _, rc in TOOL_CASES if tc == tool_name and ep == endpoint)
    url = (
        endpoint
        if endpoint.startswith("https://")
        else f"https://api.stlouisfed.org/fred/{endpoint}"
    )
    route = respx.get(url).mock(return_value=httpx.Response(200, json={response_key: []}))
    await mcp.call_tool(tool_name, arguments=args)
    actual_params = dict(route.calls.last.request.url.params)
    for key, value in expected_params.items():
        assert actual_params.get(key) == value, (
            f"Expected param {key}={value!r}, got {actual_params.get(key)!r}"
        )
    assert "api_key" in actual_params
    assert actual_params.get("file_type") == "json"


# ---------------------------------------------------------------------------
# Test 3: validation rejects both tag_names and related_to
# ---------------------------------------------------------------------------

VALIDATION_ERROR_CASES = [
    ("fred_category_tags", {"category_id": 125, "tag_names": "gdp", "related_to": "usa"}),
    ("fred_release_tags", {"release_id": 53, "tag_names": "gdp", "related_to": "usa"}),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("tool_name,args", VALIDATION_ERROR_CASES)
async def test_tags_validation_rejects_both(tool_name, args):
    with pytest.raises(ToolError):
        await mcp.call_tool(tool_name, arguments=args)


# ---------------------------------------------------------------------------
# Test 4: related_to switches endpoint
# ---------------------------------------------------------------------------

RELATED_TO_CASES = [
    (
        "fred_category_tags",
        "category/related_tags",
        {"category_id": 125, "related_to": "usa"},
        "tags",
    ),
    (
        "fred_release_tags",
        "release/related_tags",
        {"release_id": 53, "related_to": "usa"},
        "tags",
    ),
]


@respx.mock
@pytest.mark.asyncio
@pytest.mark.parametrize("tool_name,endpoint,args,response_key", RELATED_TO_CASES)
async def test_related_to_switches_endpoint(tool_name, endpoint, args, response_key):
    route = respx.get(f"https://api.stlouisfed.org/fred/{endpoint}").mock(
        return_value=httpx.Response(200, json={response_key: []})
    )
    result = await mcp.call_tool(tool_name, arguments=args)
    assert result.structured_content is not None
    assert response_key in result.structured_content
    assert route.called, f"Expected endpoint {endpoint!r} to be called"


# ---------------------------------------------------------------------------
# Test 5: None params are stripped from the HTTP request
# ---------------------------------------------------------------------------


@respx.mock
@pytest.mark.asyncio
async def test_none_params_stripped():
    route = respx.get("https://api.stlouisfed.org/fred/series").mock(
        return_value=httpx.Response(200, json={"seriess": []})
    )
    await mcp.call_tool(
        "fred_series",
        arguments={"series_id": "GNPCA", "realtime_start": None, "realtime_end": None},
    )
    actual_params = dict(route.calls.last.request.url.params)
    assert "realtime_start" not in actual_params
    assert "realtime_end" not in actual_params
