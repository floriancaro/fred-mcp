from __future__ import annotations

from typing import Literal

from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from fred_mcp.client import FredClient, get_client

mcp = FastMCP("series")


@mcp.tool
async def fred_series(
    series_id: str,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get metadata for a FRED series.

    Returns: dict with key 'seriess' containing a list of series metadata objects.
    """
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
    search_type: Literal["full_text", "series_id"] | None = None,
    realtime_start: str | None = None,
    realtime_end: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
    order_by: Literal[
        "search_rank",
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
    """Search for FRED series by text.

    Args:
        search_text: Search query (e.g., "GDP", "unemployment rate").
        search_type: "full_text" for full-text search, "series_id" to search series IDs.
        realtime_start: Start of real-time period (YYYY-MM-DD).
        realtime_end: End of real-time period (YYYY-MM-DD).
        limit: Max number of results.
        offset: Pagination offset.
        order_by: Sort results by this field.
        sort_order: "asc" or "desc".
        filter_variable: Filter by "frequency", "units", or "seasonal_adjustment".
        filter_value: Value to filter by (depends on filter_variable).
        tag_names: Semicolon-delimited tag names to filter by (e.g., "usa;gdp").
        exclude_tag_names: Semicolon-delimited tag names to exclude.

    Returns: dict with key 'seriess' containing matching series.
    """
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
    sort_order: Literal["asc", "desc"] | None = None,
    observation_start: str | None = None,
    observation_end: str | None = None,
    units: Literal["lin", "chg", "ch1", "pch", "pc1", "pca", "cch", "cca", "log"] | None = None,
    frequency: Literal[
        "d",
        "w",
        "bw",
        "m",
        "q",
        "sa",
        "a",
        "wef",
        "weth",
        "wew",
        "wetu",
        "wem",
        "wesu",
        "wesa",
    ]
    | None = None,
    aggregation_method: Literal["avg", "sum", "eop"] | None = None,
    output_type: Literal[1, 2, 3, 4] | None = None,
    vintage_dates: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get observations (data values) for a FRED series.

    Args:
        series_id: FRED series ID (e.g., "GNPCA", "UNRATE").
        realtime_start: Start of real-time period (YYYY-MM-DD).
        realtime_end: End of real-time period (YYYY-MM-DD).
        limit: Max number of results.
        offset: Pagination offset.
        sort_order: "asc" or "desc" by observation date.
        observation_start: Start of observation range (YYYY-MM-DD).
        observation_end: End of observation range (YYYY-MM-DD).
        units: Data transformation — "lin" (levels), "chg" (change), "ch1" (change from year ago),
            "pch" (percent change), "pc1" (percent change from year ago), "pca" (compounded annual
            rate of change), "cch" (continuously compounded rate of change), "cca" (continuously
            compounded annual rate of change), "log" (natural log).
        frequency: Aggregation frequency — "d" (daily), "w" (weekly), "bw" (biweekly),
            "m" (monthly), "q" (quarterly), "sa" (semiannual), "a" (annual).
            Weekly variants: "wef" (Fri), "weth" (Thu), "wew" (Wed), "wetu" (Tue),
            "wem" (Mon), "wesu" (Sun), "wesa" (Sat).
        aggregation_method: How to aggregate — "avg" (average), "sum", "eop" (end of period).
        output_type: 1=observations by real-time period, 2=all by vintage date,
            3=new/revised by vintage date, 4=initial release only.
        vintage_dates: Comma-separated vintage dates (YYYY-MM-DD).

    Returns: dict with key 'observations' containing data points with 'date' and 'value' fields.
    """
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
    """Get the categories for a FRED series.

    Returns: dict with key 'categories'.
    """
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
    """Get the release for a FRED series.

    Returns: dict with key 'releases'.
    """
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
    """Get the FRED tags for a series.

    Returns: dict with key 'tags'.
    """
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
    tag_group_id: Literal["freq", "gen", "geo", "geot", "rls", "seas", "src", "cc"] | None = None,
    tag_search_text: str | None = None,
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
    """Get the tags for a series search query.

    Returns: dict with key 'tags'.
    """
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
    tag_group_id: Literal["freq", "gen", "geo", "geot", "rls", "seas", "src", "cc"] | None = None,
    tag_search_text: str | None = None,
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
    """Get related tags for a series search, filtered by specified tags.

    Returns: dict with key 'tags'.
    """
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
    filter_value: Literal["macro", "regional", "all"] | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get recently updated FRED series.

    Args:
        realtime_start: Start of real-time period (YYYY-MM-DD).
        realtime_end: End of real-time period (YYYY-MM-DD).
        limit: Max number of results.
        offset: Pagination offset.
        filter_value: "macro" for macroeconomic series, "regional" for regional, "all" for both.
        start_time: Filter to series updated on or after this time (YYYYMMDDHhmm format).
        end_time: Filter to series updated on or before this time (YYYYMMDDHhmm format).

    Returns: dict with key 'seriess' containing recently updated series.
    """
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
    sort_order: Literal["asc", "desc"] | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get vintage dates (revision history) for a FRED series.

    Returns: dict with key 'vintage_dates'.
    """
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
