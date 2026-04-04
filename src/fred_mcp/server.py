from contextlib import asynccontextmanager

from fastmcp import FastMCP
from fastmcp.server.middleware.logging import LoggingMiddleware

from fred_mcp.client import reset_client
from fred_mcp.tools.categories import mcp as categories
from fred_mcp.tools.geo import mcp as geo
from fred_mcp.tools.releases import mcp as releases
from fred_mcp.tools.series import mcp as series
from fred_mcp.tools.sources import mcp as sources
from fred_mcp.tools.tags import mcp as tags


@asynccontextmanager
async def lifespan(server):
    yield {}
    await reset_client()


mcp = FastMCP(
    "fred",
    lifespan=lifespan,
    instructions=(
        "Access the Federal Reserve Economic Data (FRED) API. "
        "Search for economic time series, retrieve observations, "
        "explore categories, releases, sources, and tags. "
        "Also supports the Maps API for regional/geographic data and shape files. "
        "All date parameters use YYYY-MM-DD format."
    ),
)
mcp.add_middleware(LoggingMiddleware())
mcp.mount(categories)
mcp.mount(releases)
mcp.mount(series)
mcp.mount(sources)
mcp.mount(tags)
mcp.mount(geo)


def main():
    mcp.run()
