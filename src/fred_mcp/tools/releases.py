from __future__ import annotations

from fastmcp.dependencies import Depends

from fred_mcp.server import mcp, get_client
from fred_mcp.client import FredClient


@mcp.tool
async def fred_releases(
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: str | None = None,
    sort_order: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get all FRED releases of economic data."""
    return await client.get(
        "releases",
        {
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "offset": offset,
            "order_by": order_by,
            "sort_order": sort_order,
        },
    )


@mcp.tool
async def fred_releases_dates(
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: str | None = None,
    sort_order: str | None = None,
    include_release_dates_with_no_data: bool | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get release dates for all FRED releases."""
    return await client.get(
        "releases/dates",
        {
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "offset": offset,
            "order_by": order_by,
            "sort_order": sort_order,
            "include_release_dates_with_no_data": include_release_dates_with_no_data,
        },
    )


@mcp.tool
async def fred_release(
    release_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get a specific FRED release of economic data."""
    return await client.get(
        "release",
        {
            "release_id": release_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
        },
    )


@mcp.tool
async def fred_release_dates(
    release_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    sort_order: str | None = None,
    include_release_dates_with_no_data: bool | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get release dates for a specific FRED release."""
    return await client.get(
        "release/dates",
        {
            "release_id": release_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "offset": offset,
            "sort_order": sort_order,
            "include_release_dates_with_no_data": include_release_dates_with_no_data,
        },
    )


@mcp.tool
async def fred_release_series(
    release_id: int,
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
    """Get the series on a FRED release."""
    return await client.get(
        "release/series",
        {
            "release_id": release_id,
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
async def fred_release_sources(
    release_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get the sources for a FRED release."""
    return await client.get(
        "release/sources",
        {
            "release_id": release_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
        },
    )


@mcp.tool
async def fred_release_tags(
    release_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    tag_names: str | None = None,
    tag_group_id: str | None = None,
    search_text: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: str | None = None,
    sort_order: str | None = None,
    related_to: str | None = None,
    exclude_tag_names: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get tags for a FRED release. Use related_to to filter to tags related to specified semicolon-delimited tag names."""
    endpoint = "release/related_tags" if related_to else "release/tags"
    params = {
        "release_id": release_id,
        "realtime_start": realtime_start,
        "realtime_end": realtime_end,
        "tag_names": related_to if related_to else tag_names,
        "tag_group_id": tag_group_id,
        "search_text": search_text,
        "limit": limit,
        "offset": offset,
        "order_by": order_by,
        "sort_order": sort_order,
        "exclude_tag_names": exclude_tag_names,
    }
    return await client.get(endpoint, params)


@mcp.tool
async def fred_release_tables(
    release_id: int,
    element_id: int | None = None,
    include_observation_values: bool | None = None,
    observation_date: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get release table trees for a FRED release."""
    return await client.get(
        "release/tables",
        {
            "release_id": release_id,
            "element_id": element_id,
            "include_observation_values": include_observation_values,
            "observation_date": observation_date,
        },
    )
