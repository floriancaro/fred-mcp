from __future__ import annotations

from typing import Literal

from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from fred_mcp.client import FredClient, get_client

mcp = FastMCP("tags")


@mcp.tool
async def fred_tags(
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    tag_names: str | None = None,
    tag_group_id: Literal["freq", "gen", "geo", "geot", "rls", "seas", "src", "cc"] | None = None,
    search_text: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: Literal[
        "series_count",
        "popularity",
        "created",
        "name",
        "group_id",
    ]
    | None = None,
    sort_order: Literal["asc", "desc"] | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get all FRED tags, optionally filtered by name or group.

    Returns: dict with key 'tags'.
    """
    return await client.get(
        "tags",
        {
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "tag_names": tag_names,
            "tag_group_id": tag_group_id,
            "search_text": search_text,
            "limit": limit,
            "offset": offset,
            "order_by": order_by,
            "sort_order": sort_order,
        },
    )


@mcp.tool
async def fred_related_tags(
    tag_names: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    exclude_tag_names: str | None = None,
    tag_group_id: Literal["freq", "gen", "geo", "geot", "rls", "seas", "src", "cc"] | None = None,
    search_text: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: Literal[
        "series_count",
        "popularity",
        "created",
        "name",
        "group_id",
    ]
    | None = None,
    sort_order: Literal["asc", "desc"] | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get tags related to specified semicolon-delimited tag names.

    Returns: dict with key 'tags'.
    """
    return await client.get(
        "related_tags",
        {
            "tag_names": tag_names,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "exclude_tag_names": exclude_tag_names,
            "tag_group_id": tag_group_id,
            "search_text": search_text,
            "limit": limit,
            "offset": offset,
            "order_by": order_by,
            "sort_order": sort_order,
        },
    )


@mcp.tool
async def fred_tags_series(
    tag_names: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    exclude_tag_names: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: Literal[
        "series_id",
        "title",
        "units",
        "frequency",
        "seasonal_adjustment",
        "realtime_start",
        "realtime_end",
        "last_updated",
        "observation_start",
        "observation_end",
        "popularity",
        "group_popularity",
    ]
    | None = None,
    sort_order: Literal["asc", "desc"] | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get series matching all specified semicolon-delimited tag names.

    Returns: dict with key 'seriess'.
    """
    return await client.get(
        "tags/series",
        {
            "tag_names": tag_names,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "exclude_tag_names": exclude_tag_names,
            "limit": limit,
            "offset": offset,
            "order_by": order_by,
            "sort_order": sort_order,
        },
    )
