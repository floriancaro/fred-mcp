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
