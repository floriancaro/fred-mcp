from __future__ import annotations

from typing import Literal

from fastmcp import FastMCP
from fastmcp.dependencies import Depends
from fastmcp.exceptions import ToolError

from fred_mcp.client import FredClient, get_client

mcp = FastMCP("categories")


@mcp.tool
async def fred_category(
    category_id: int = 0,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get a FRED category. Use category_id=0 for the root category.

    Returns: dict with key 'categories'.
    """
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
    """Get the child categories for a FRED category.

    Returns: dict with key 'categories'.
    """
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
    """Get the related categories for a FRED category.

    Returns: dict with key 'categories'.
    """
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
    filter_variable: Literal["frequency", "units", "seasonal_adjustment"] | None = None,
    filter_value: str | None = None,
    tag_names: str | None = None,
    exclude_tag_names: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get the series in a FRED category.

    Returns: dict with key 'seriess'.
    """
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
    related_to: str | None = None,
    exclude_tag_names: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get tags for a FRED category, or find related tags.

    When related_to is set, returns tags related to the specified tag names
    (uses the category/related_tags endpoint). Otherwise returns all tags
    for the category.

    Args:
        category_id: FRED category ID.
        realtime_start: Start of real-time period (YYYY-MM-DD).
        realtime_end: End of real-time period (YYYY-MM-DD).
        tag_names: Semicolon-delimited tag names to filter by.
        tag_group_id: Tag group to filter by.
        search_text: Search tags by text.
        limit: Max number of results.
        offset: Pagination offset.
        order_by: Sort results by this field.
        sort_order: "asc" or "desc".
        related_to: Semicolon-delimited tag names to find related tags for.
            When set, tag_names is ignored and the related_tags endpoint is used.
        exclude_tag_names: Semicolon-delimited tag names to exclude.

    Returns: dict with key 'tags'.
    """
    if related_to and tag_names:
        raise ToolError(
            "Cannot use both tag_names and related_to. "
            "Use related_to to specify the tags to find related tags for."
        )
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
