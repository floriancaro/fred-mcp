from __future__ import annotations

from fastmcp.dependencies import Depends
from fastmcp.exceptions import ToolError

from fred_mcp.server import mcp, get_client
from fred_mcp.client import FredClient


@mcp.tool
async def fred_category(
    category_id: int = 0,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get a FRED category. Use category_id=0 for the root category."""
    return await client.get(
        "category",
        {
            "category_id": category_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
        },
    )


@mcp.tool
async def fred_category_children(
    category_id: int = 0,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get the child categories for a FRED category."""
    return await client.get(
        "category/children",
        {
            "category_id": category_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
        },
    )


@mcp.tool
async def fred_category_related(
    category_id: int,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get the related categories for a FRED category."""
    return await client.get(
        "category/related",
        {
            "category_id": category_id,
            "realtime_start": realtime_start,
            "realtime_end": realtime_end,
        },
    )


@mcp.tool
async def fred_category_series(
    category_id: int,
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
    """Get the series in a FRED category."""
    return await client.get(
        "category/series",
        {
            "category_id": category_id,
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
async def fred_category_tags(
    category_id: int,
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
    """Get tags for a FRED category. Use related_to to filter to tags related to specified semicolon-delimited tag names. When related_to is set, tag_names is ignored."""
    if related_to and tag_names:
        raise ToolError("Cannot use both tag_names and related_to. Use related_to to specify the tags to find related tags for.")
    endpoint = "category/related_tags" if related_to else "category/tags"
    params = {
        "category_id": category_id,
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
