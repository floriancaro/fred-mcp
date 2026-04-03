import os
import pytest
from fred_mcp.client import FredClient

HAVE_API_KEY = bool(os.environ.get("FRED_API_KEY"))

integration = pytest.mark.skipif(
    not HAVE_API_KEY, reason="FRED_API_KEY not set"
)


@pytest.fixture
async def live_client():
    """FredClient for integration tests. Only usable when FRED_API_KEY is set."""
    client = FredClient()
    yield client
    await client.close()
