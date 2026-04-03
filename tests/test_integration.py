import os

import pytest

integration = pytest.mark.skipif(
    not bool(os.environ.get("FRED_API_KEY")), reason="FRED_API_KEY not set"
)


# --- Series ---

@integration
@pytest.mark.asyncio
async def test_series(live_client):
    result = await live_client.get("series", {"series_id": "GNPCA"})
    assert "seriess" in result
    assert result["seriess"][0]["id"] == "GNPCA"


@integration
@pytest.mark.asyncio
async def test_series_search(live_client):
    result = await live_client.get("series/search", {"search_text": "gdp", "limit": 2})
    assert "seriess" in result
    assert len(result["seriess"]) <= 2


@integration
@pytest.mark.asyncio
async def test_series_observations(live_client):
    result = await live_client.get("series/observations", {"series_id": "GNPCA", "limit": 5})
    assert "observations" in result
    assert len(result["observations"]) <= 5


@integration
@pytest.mark.asyncio
async def test_series_categories(live_client):
    result = await live_client.get("series/categories", {"series_id": "EXJPUS"})
    assert "categories" in result


@integration
@pytest.mark.asyncio
async def test_series_release(live_client):
    result = await live_client.get("series/release", {"series_id": "IRA"})
    assert "releases" in result


@integration
@pytest.mark.asyncio
async def test_series_tags(live_client):
    result = await live_client.get("series/tags", {"series_id": "STLFSI"})
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_series_search_tags(live_client):
    result = await live_client.get("series/search/tags", {"series_search_text": "monetary service index", "limit": 3})
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_series_search_related_tags(live_client):
    result = await live_client.get(
        "series/search/related_tags",
        {"series_search_text": "mortgage rate", "tag_names": "30-year;frb", "limit": 3},
    )
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_series_updates(live_client):
    result = await live_client.get("series/updates", {"limit": 3})
    assert "seriess" in result


@integration
@pytest.mark.asyncio
async def test_series_vintagedates(live_client):
    result = await live_client.get("series/vintagedates", {"series_id": "GNPCA", "limit": 5})
    assert "vintage_dates" in result


# --- Categories ---

@integration
@pytest.mark.asyncio
async def test_category(live_client):
    result = await live_client.get("category", {"category_id": 125})
    assert "categories" in result
    assert result["categories"][0]["id"] == 125


@integration
@pytest.mark.asyncio
async def test_category_children(live_client):
    result = await live_client.get("category/children", {"category_id": 13})
    assert "categories" in result


@integration
@pytest.mark.asyncio
async def test_category_related(live_client):
    result = await live_client.get("category/related", {"category_id": 32073})
    assert "categories" in result


@integration
@pytest.mark.asyncio
async def test_category_series(live_client):
    result = await live_client.get("category/series", {"category_id": 125, "limit": 2})
    assert "seriess" in result


@integration
@pytest.mark.asyncio
async def test_category_tags(live_client):
    result = await live_client.get("category/tags", {"category_id": 125, "limit": 3})
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_category_related_tags(live_client):
    result = await live_client.get(
        "category/related_tags",
        {"category_id": 125, "tag_names": "services;quarterly", "limit": 3},
    )
    assert "tags" in result


# --- Releases ---

@integration
@pytest.mark.asyncio
async def test_releases(live_client):
    result = await live_client.get("releases", {"limit": 3})
    assert "releases" in result


@integration
@pytest.mark.asyncio
async def test_releases_dates(live_client):
    result = await live_client.get("releases/dates", {"limit": 3})
    assert "release_dates" in result


@integration
@pytest.mark.asyncio
async def test_release(live_client):
    result = await live_client.get("release", {"release_id": 53})
    assert "releases" in result


@integration
@pytest.mark.asyncio
async def test_release_dates(live_client):
    result = await live_client.get("release/dates", {"release_id": 82, "limit": 3})
    assert "release_dates" in result


@integration
@pytest.mark.asyncio
async def test_release_series(live_client):
    result = await live_client.get("release/series", {"release_id": 51, "limit": 2})
    assert "seriess" in result


@integration
@pytest.mark.asyncio
async def test_release_sources(live_client):
    result = await live_client.get("release/sources", {"release_id": 51})
    assert "sources" in result


@integration
@pytest.mark.asyncio
async def test_release_tags(live_client):
    result = await live_client.get("release/tags", {"release_id": 86, "limit": 3})
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_release_related_tags(live_client):
    result = await live_client.get(
        "release/related_tags",
        {"release_id": 86, "tag_names": "sa;foreign", "limit": 3},
    )
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_release_tables(live_client):
    result = await live_client.get("release/tables", {"release_id": 53, "element_id": 12886})
    assert "elements" in result


# --- Sources ---

@integration
@pytest.mark.asyncio
async def test_sources(live_client):
    result = await live_client.get("sources", {"limit": 3})
    assert "sources" in result


@integration
@pytest.mark.asyncio
async def test_source(live_client):
    result = await live_client.get("source", {"source_id": 1})
    assert "sources" in result


@integration
@pytest.mark.asyncio
async def test_source_releases(live_client):
    result = await live_client.get("source/releases", {"source_id": 1, "limit": 3})
    assert "releases" in result


# --- Tags ---

@integration
@pytest.mark.asyncio
async def test_tags(live_client):
    result = await live_client.get("tags", {"limit": 3})
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_related_tags(live_client):
    result = await live_client.get(
        "related_tags",
        {"tag_names": "monetary aggregates;weekly", "limit": 3},
    )
    assert "tags" in result


@integration
@pytest.mark.asyncio
async def test_tags_series(live_client):
    result = await live_client.get(
        "tags/series",
        {"tag_names": "slovenia;food;oecd", "limit": 2},
    )
    assert "seriess" in result
