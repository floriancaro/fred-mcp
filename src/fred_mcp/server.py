from fastmcp import FastMCP
from fastmcp.dependencies import Depends

from fred_mcp.client import FredClient

mcp = FastMCP("fred")

_client: FredClient | None = None


def get_client() -> FredClient:
    global _client
    if _client is None:
        _client = FredClient()
    return _client


# Tool registrations (import triggers @mcp.tool decorators)
import fred_mcp.tools.series  # noqa: F401
import fred_mcp.tools.categories  # noqa: F401
import fred_mcp.tools.releases  # noqa: F401
import fred_mcp.tools.sources  # noqa: F401
import fred_mcp.tools.tags  # noqa: F401


def main():
    mcp.run()
