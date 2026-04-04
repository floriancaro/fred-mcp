from __future__ import annotations

from typing import Literal

from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from fred_mcp.client import FredClient, get_client

mcp = FastMCP("sources")


@mcp.tool
async def fred_sources(
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: str | None = None,
    sort_order: Literal["asc", "desc"] | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get all sources of economic data."""
    return await client.get(
        "sources",
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
async def fred_source(
    source_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get a specific source of economic data."""
    return await client.get(
        "source",
        {
            "source_id": source_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
        },
    )


@mcp.tool
async def fred_source_releases(
    source_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: str | None = None,
    sort_order: Literal["asc", "desc"] | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get the releases for a source."""
    return await client.get(
        "source/releases",
        {
            "source_id": source_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
            "limit": limit,
            "offset": offset,
            "order_by": order_by,
            "sort_order": sort_order,
        },
    )
