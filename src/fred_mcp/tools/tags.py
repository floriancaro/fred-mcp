from __future__ import annotations

from fastmcp.dependencies import Depends

from fred_mcp.server import mcp, get_client
from fred_mcp.client import FredClient


@mcp.tool
async def fred_tags(
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    tag_names: str | None = None,
    tag_group_id: str | None = None,
    search_text: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: str | None = None,
    sort_order: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get all FRED tags, optionally filtered by name or group."""
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
    tag_group_id: str | None = None,
    search_text: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: str | None = None,
    sort_order: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get tags related to specified semicolon-delimited tag names."""
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
    order_by: str | None = None,
    sort_order: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get series matching all specified semicolon-delimited tag names."""
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
