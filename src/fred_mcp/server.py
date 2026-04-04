from contextlib import asynccontextmanager

from fastmcp import FastMCP

from fred_mcp.client import get_client
from fred_mcp.tools.categories import mcp as categories
from fred_mcp.tools.geo import mcp as geo
from fred_mcp.tools.releases import mcp as releases
from fred_mcp.tools.series import mcp as series
from fred_mcp.tools.sources import mcp as sources
from fred_mcp.tools.tags import mcp as tags


@asynccontextmanager
async def lifespan(server):
    yield {}
    client = await get_client()
    await client.close()


mcp = FastMCP("fred", lifespan=lifespan)
mcp.mount(categories)
mcp.mount(releases)
mcp.mount(series)
mcp.mount(sources)
mcp.mount(tags)
mcp.mount(geo)


def main():
    mcp.run()
