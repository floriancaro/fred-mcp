from __future__ import annotations

from typing import Literal

from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from fred_mcp.client import GEOFRED_BASE_URL, FredClient, get_client

mcp = FastMCP("geo")


@mcp.tool
async def geofred_series_group(
    series_id: str,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get metadata for a geographic FRED series.

    Returns metadata including title, region type, series group ID, seasonality,
    units, frequency, and date range.

    Returns: dict with key 'series_group'.
    """
    return await client.get(
        "series/group",
        {"series_id": series_id},
        base_url=GEOFRED_BASE_URL,
    )


@mcp.tool
async def geofred_series_data(
    series_id: str,
    date: str | None = None,
    start_date: str | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get cross-sectional regional data for a geographic FRED series.

    Args:
        series_id: FRED series ID (e.g., "WIPCPI").
        date: Observation date (YYYY-MM-DD). Returns data for this specific date.
        start_date: Start of date range (YYYY-MM-DD). Returns data from this date onward.

    Returns: dict with keys 'meta' and 'data'.
    """
    return await client.get(
        "series/data",
        {
            "series_id": series_id,
            "date": date,
            "start_date": start_date,
        },
        base_url=GEOFRED_BASE_URL,
    )


@mcp.tool
async def geofred_regional_data(
    series_group: str,
    region_type: Literal[
        "bea", "msa", "frb", "necta", "state", "country", "county", "censusregion"
    ],
    date: str,
    season: Literal["SA", "NSA", "SSA", "SAAR", "NSAAR"],
    units: str,
    start_date: str | None = None,
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
        "bwew",
        "bwem",
    ]
    | None = None,
    transformation: Literal["lin", "chg", "ch1", "pch", "pc1", "pca", "cch", "cca", "log"]
    | None = None,
    aggregation_method: Literal["avg", "sum", "eop"] | None = None,
    client: FredClient = Depends(get_client),
) -> dict:
    """Get cross-sectional regional data by series group.

    Args:
        series_group: Series group ID (get from geofred_series_group).
        region_type: Geographic region type.
        date: Observation date (YYYY-MM-DD).
        season: Seasonal adjustment — "SA" (adjusted), "NSA" (not adjusted),
            "SSA" (smoothed adjusted), "SAAR"/"NSAAR" (annualized rates).
        units: Unit description string (e.g., "Dollars", "Percent").
        start_date: Start of date range (YYYY-MM-DD).
        frequency: Aggregation frequency.
        transformation: Data transformation (same codes as series observations units).
        aggregation_method: How to aggregate — "avg", "sum", "eop".

    Returns: dict with keys 'meta' and 'data'.
    """
    return await client.get(
        "regional/data",
        {
            "series_group": series_group,
            "region_type": region_type,
            "date": date,
            "season": season,
            "units": units,
            "start_date": start_date,
            "frequency": frequency,
            "transformation": transformation,
            "aggregation_method": aggregation_method,
        },
        base_url=GEOFRED_BASE_URL,
    )


@mcp.tool
async def geofred_shapes(
    shape: Literal[
        "bea",
        "msa",
        "frb",
        "necta",
        "state",
        "country",
        "county",
        "censusregion",
        "censusdivision",
    ],
    client: FredClient = Depends(get_client),
) -> dict:
    """Get GeoJSON shape files for geographic region boundaries.

    Warning: county-level shapes can be very large (several MB of coordinate data).
    Prefer state or broader region types when possible.

    Args:
        shape: Region type for shape boundaries.

    Returns: GeoJSON FeatureCollection with 'type' and 'features' keys.
    """
    return await client.get(
        "shapes/file",
        {"shape": shape},
        base_url=GEOFRED_BASE_URL,
    )
