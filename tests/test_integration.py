import os
import pytest
from fred_mcp.client import FredClient

integration = pytest.mark.skipif(
    not bool(os.environ.get("FRED_API_KEY")), reason="FRED_API_KEY not set"
)


@pytest.fixture
async def client():
    c = FredClient()
    yield c
    await c.close()


# --- Series ---

@integration
@pytest.mark.asyncio
async def test_series(client):
    result = await client.get("series", {"series_id": "GNPCA"})
    assert "seriess" in result
    assert result["seriess"][0]["id"] == "GNPCA"


@integration
@pytest.mark.asyncio
async def test_series_search(client):
    result = await client.get("series/search", {"search_text": "gdp", "limit": 2})
    assert "seriess" in result
    assert len(result["seriess"]) <= 2


@integration
@pytest.mark.asyncio
async def test_series_observations(client):
    result = await client.get("series/observations", {"series_id": "GNPCA", "limit": 5})
    assert "observations" in result
    assert len(result["observations"]) <= 5


@integration
@pytest.mark.asyncio
async def test_series_categories(client):
    result = await client.get("series/categories", {"series_id": "EXJPUS"})
    assert "categories" in result


@integration
@pytest.mark.asyncio
async def test_series_release(client):
    result = await client.get("series/release", {"series_id": "IRA"})
    assert "releases" in result


@integration
@pytest.mark.asyncio
async def test_series_tags(client):
    result = await client.get("series/tags", {"series_id": "STLFSI"})
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_series_search_tags(client):
    result = await client.get("series/search/tags", {"series_search_text": "monetary service index", "limit": 3})
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_series_search_related_tags(client):
    result = await client.get(
        "series/search/related_tags",
        {"series_search_text": "mortgage rate", "tag_names": "30-year;frb", "limit": 3},
    )
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_series_updates(client):
    result = await client.get("series/updates", {"limit": 3})
    assert "seriess" in result


@integration
@pytest.mark.asyncio
async def test_series_vintagedates(client):
    result = await client.get("series/vintagedates", {"series_id": "GNPCA", "limit": 5})
    assert "vintage_dates" in result


# --- Categories ---

@integration
@pytest.mark.asyncio
async def test_category(client):
    result = await client.get("category", {"category_id": 125})
    assert "categories" in result
    assert result["categories"][0]["id"] == 125


@integration
@pytest.mark.asyncio
async def test_category_children(client):
    result = await client.get("category/children", {"category_id": 13})
    assert "categories" in result


@integration
@pytest.mark.asyncio
async def test_category_related(client):
    result = await client.get("category/related", {"category_id": 32073})
    assert "categories" in result


@integration
@pytest.mark.asyncio
async def test_category_series(client):
    result = await client.get("category/series", {"category_id": 125, "limit": 2})
    assert "seriess" in result


@integration
@pytest.mark.asyncio
async def test_category_tags(client):
    result = await client.get("category/tags", {"category_id": 125, "limit": 3})
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_category_related_tags(client):
    result = await client.get(
        "category/related_tags",
        {"category_id": 125, "tag_names": "services;quarterly", "limit": 3},
    )
    assert "tags" in result


# --- Releases ---

@integration
@pytest.mark.asyncio
async def test_releases(client):
    result = await client.get("releases", {"limit": 3})
    assert "releases" in result


@integration
@pytest.mark.asyncio
async def test_releases_dates(client):
    result = await client.get("releases/dates", {"limit": 3})
    assert "release_dates" in result


@integration
@pytest.mark.asyncio
async def test_release(client):
    result = await client.get("release", {"release_id": 53})
    assert "releases" in result


@integration
@pytest.mark.asyncio
async def test_release_dates(client):
    result = await client.get("release/dates", {"release_id": 82, "limit": 3})
    assert "release_dates" in result


@integration
@pytest.mark.asyncio
async def test_release_series(client):
    result = await client.get("release/series", {"release_id": 51, "limit": 2})
    assert "seriess" in result


@integration
@pytest.mark.asyncio
async def test_release_sources(client):
    result = await client.get("release/sources", {"release_id": 51})
    assert "sources" in result


@integration
@pytest.mark.asyncio
async def test_release_tags(client):
    result = await client.get("release/tags", {"release_id": 86, "limit": 3})
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_release_related_tags(client):
    result = await client.get(
        "release/related_tags",
        {"release_id": 86, "tag_names": "sa;foreign", "limit": 3},
    )
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_release_tables(client):
    result = await client.get("release/tables", {"release_id": 53, "element_id": 12886})
    assert "elements" in result


# --- Sources ---

@integration
@pytest.mark.asyncio
async def test_sources(client):
    result = await client.get("sources", {"limit": 3})
    assert "sources" in result


@integration
@pytest.mark.asyncio
async def test_source(client):
    result = await client.get("source", {"source_id": 1})
    assert "sources" in result


@integration
@pytest.mark.asyncio
async def test_source_releases(client):
    result = await client.get("source/releases", {"source_id": 1, "limit": 3})
    assert "releases" in result


# --- Tags ---

@integration
@pytest.mark.asyncio
async def test_tags(client):
    result = await client.get("tags", {"limit": 3})
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_related_tags(client):
    result = await client.get(
        "related_tags",
        {"tag_names": "monetary aggregates;weekly", "limit": 3},
    )
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_tags_series(client):
    result = await client.get(
        "tags/series",
        {"tag_names": "slovenia;food;oecd", "limit": 2},
    )
    assert "seriess" in result
