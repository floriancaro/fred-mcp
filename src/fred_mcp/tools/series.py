from __future__ import annotations

from fastmcp.dependencies import Depends

from fred_mcp.server import mcp, get_client
from fred_mcp.client import FredClient


@mcp.tool
async def fred_series(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get metadata for a FRED series."""
    return await client.get(
        "series",
        {
            "series_id": series_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
        },
    )


@mcp.tool
async def fred_series_search(
    search_text: str,
    search_type: str | None = None,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: str | None = None,
    sort_order: str | None = None,
    filter_variable: str | None = None,
    filter_value: str | None = None,
    tag_names: str | None = None,
    exclude_tag_names: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Search for FRED series by text. Set search_type='full_text' for full-text search or 'series_id' to search IDs."""
    return await client.get(
        "series/search",
        {
            "search_text": search_text,
            "search_type": search_type,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "offset": offset,
            "order_by": order_by,
            "sort_order": sort_order,
            "filter_variable": filter_variable,
            "filter_value": filter_value,
            "tag_names": tag_names,
            "exclude_tag_names": exclude_tag_names,
        },
    )


@mcp.tool
async def fred_series_observations(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    sort_order: str | None = None,
    observation_start: str | None = None,
    observation_end: str | None = None,
    units: str | None = None,
    frequency: str | None = None,
    aggregation_method: str | None = None,
    output_type: int | None = None,
    vintage_dates: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get observations (data values) for a FRED series."""
    return await client.get(
        "series/observations",
        {
            "series_id": series_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "offset": offset,
            "sort_order": sort_order,
            "observation_start": observation_start,
            "observation_end": observation_end,
            "units": units,
            "frequency": frequency,
            "aggregation_method": aggregation_method,
            "output_type": output_type,
            "vintage_dates": vintage_dates,
        },
    )


@mcp.tool
async def fred_series_categories(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get the categories for a FRED series."""
    return await client.get(
        "series/categories",
        {
            "series_id": series_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
        },
    )


@mcp.tool
async def fred_series_release(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get the release for a FRED series."""
    return await client.get(
        "series/release",
        {
            "series_id": series_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
        },
    )


@mcp.tool
async def fred_series_tags(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    order_by: str | None = None,
    sort_order: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get the FRED tags for a series."""
    return await client.get(
        "series/tags",
        {
            "series_id": series_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "order_by": order_by,
            "sort_order": sort_order,
        },
    )


@mcp.tool
async def fred_series_search_tags(
    series_search_text: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    tag_names: str | None = None,
    tag_group_id: str | None = None,
    tag_search_text: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: str | None = None,
    sort_order: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get the tags for a series search query."""
    return await client.get(
        "series/search/tags",
        {
            "series_search_text": series_search_text,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "tag_names": tag_names,
            "tag_group_id": tag_group_id,
            "tag_search_text": tag_search_text,
            "limit": limit,
            "offset": offset,
            "order_by": order_by,
            "sort_order": sort_order,
        },
    )


@mcp.tool
async def fred_series_search_related_tags(
    series_search_text: str,
    tag_names: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    exclude_tag_names: str | None = None,
    tag_group_id: str | None = None,
    tag_search_text: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: str | None = None,
    sort_order: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get related tags for a series search, filtered by specified tags."""
    return await client.get(
        "series/search/related_tags",
        {
            "series_search_text": series_search_text,
            "tag_names": tag_names,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "exclude_tag_names": exclude_tag_names,
            "tag_group_id": tag_group_id,
            "tag_search_text": tag_search_text,
            "limit": limit,
            "offset": offset,
            "order_by": order_by,
            "sort_order": sort_order,
        },
    )


@mcp.tool
async def fred_series_updates(
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    filter_value: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get recently updated FRED series."""
    return await client.get(
        "series/updates",
        {
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "offset": offset,
            "filter_value": filter_value,
            "start_time": start_time,
            "end_time": end_time,
        },
    )


@mcp.tool
async def fred_series_vintagedates(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    sort_order: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get vintage dates (revision history) for a FRED series."""
    return await client.get(
        "series/vintagedates",
        {
            "series_id": series_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "offset": offset,
            "sort_order": sort_order,
        },
    )
