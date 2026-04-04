# fred-mcp-server

[![CI](https://github.com/floriancaro/fred-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/floriancaro/fred-mcp-server/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/fred-mcp-server)](https://pypi.org/project/fred-mcp-server/)
[![Python](https://img.shields.io/pypi/pyversions/fred-mcp-server)](https://pypi.org/project/fred-mcp-server/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An MCP (Model Context Protocol) server that provides access to the full [FRED API](https://fred.stlouisfed.org/docs/api/fred/) and [GeoFRED API](https://fred.stlouisfed.org/docs/api/geofred/) (Federal Reserve Economic Data). Use it to search, explore, and retrieve economic data directly within Claude conversations.

> **Disclaimer:** This project is not affiliated with, endorsed by, or connected to the Federal Reserve Bank of St. Louis or any Federal Reserve entity. It is an independent open-source tool that accesses the publicly available FRED API.

## Features

- **33 tools** covering all FRED and GeoFRED API endpoints (series, categories, releases, sources, tags, maps)
- Full parameter support — no artificial limits on pagination or filtering
- Built-in rate limiting (120 requests/minute)
- Async HTTP client for efficient request handling

## Requirements

- Python 3.10+
- A free [FRED API key](https://fred.stlouisfed.org/docs/api/api_key.html)

## Installation

```bash
pip install fred-mcp-server
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv tool install fred-mcp-server
```

With Docker:

```bash
docker build -t fred-mcp-server https://github.com/floriancaro/fred-mcp-server.git
```

From source:

```bash
git clone https://github.com/floriancaro/fred-mcp-server.git
cd fred-mcp-server
pip install -e ".[dev]"
```

## Configuration

After installing, configure the MCP server for your preferred client.

### Claude Code (CLI)

Add the server globally (available in all projects):

```bash
claude mcp add fred -s user -e FRED_API_KEY=your-api-key-here -- fred-mcp-server
```

Or add it to a specific project only:

```bash
claude mcp add fred -e FRED_API_KEY=your-api-key-here -- fred-mcp-server
```

Verify it's connected:

```bash
claude mcp list
```

### Claude Code (project config)

Alternatively, create a `.mcp.json` file in your project root:

```json
{
  "mcpServers": {
    "fred": {
      "command": "fred-mcp-server",
      "env": {
        "FRED_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

A `.mcp.json.example` file is included in the repo as a template.

### Claude Desktop

Add to your Claude Desktop config file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fred": {
      "command": "fred-mcp-server",
      "env": {
        "FRED_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Restart Claude Desktop after saving.

### Docker

If using the Docker image, replace the `command` field:

```json
{
  "mcpServers": {
    "fred": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "FRED_API_KEY", "fred-mcp-server"],
      "env": {
        "FRED_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Tools

### Series

| Tool | Description |
|------|-------------|
| `fred_series` | Get metadata for a series |
| `fred_series_search` | Search for series by text |
| `fred_series_observations` | Get data values for a series |
| `fred_series_categories` | Get categories for a series |
| `fred_series_release` | Get the release for a series |
| `fred_series_tags` | Get tags for a series |
| `fred_series_search_tags` | Get tags matching a search query |
| `fred_series_search_related_tags` | Get related tags for a search query |
| `fred_series_updates` | Get recently updated series |
| `fred_series_vintagedates` | Get vintage dates for a series |

### Categories

| Tool | Description |
|------|-------------|
| `fred_category` | Get a category (root = 0) |
| `fred_category_children` | Get child categories |
| `fred_category_related` | Get related categories |
| `fred_category_series` | Get series in a category |
| `fred_category_tags` | Get tags for a category |

### Releases

| Tool | Description |
|------|-------------|
| `fred_releases` | List all releases |
| `fred_releases_dates` | Get dates for all releases |
| `fred_release` | Get a specific release |
| `fred_release_dates` | Get dates for a release |
| `fred_release_series` | Get series in a release |
| `fred_release_sources` | Get sources for a release |
| `fred_release_tags` | Get tags for a release |
| `fred_release_tables` | Get release table trees |

### Sources

| Tool | Description |
|------|-------------|
| `fred_sources` | List all sources |
| `fred_source` | Get a specific source |
| `fred_source_releases` | Get releases for a source |

### Tags

| Tool | Description |
|------|-------------|
| `fred_tags` | List/search all tags |
| `fred_related_tags` | Get related tags |
| `fred_tags_series` | Get series matching tags |

### GeoFRED (Maps)

| Tool | Description |
|------|-------------|
| `geofred_series_group` | Get metadata for a geographic FRED series |
| `geofred_series_data` | Get cross-sectional regional data for a geographic series |
| `geofred_regional_data` | Get cross-sectional regional data by series group |
| `geofred_shapes` | Get GeoJSON shape files for geographic region boundaries |

## Example Prompts

Once configured, you can ask Claude things like:

- "What is the current US GDP growth rate?" (uses `fred_series_search` + `fred_series_observations`)
- "Show me the unemployment rate for the past 10 years" (uses `fred_series_observations` with `observation_start`)
- "What data releases are coming up this week?" (uses `fred_releases_dates`)
- "Find all series related to housing starts" (uses `fred_series_search`)
- "Compare regional unemployment rates across states" (uses `geofred_regional_data`)

## Development

```bash
git clone https://github.com/floriancaro/fred-mcp-server.git
cd fred-mcp-server
pip install -e ".[dev]"

# Run unit tests
python -m pytest tests/test_client.py tests/test_tools.py -v

# Run integration tests (requires FRED_API_KEY)
FRED_API_KEY=your-key python -m pytest tests/test_integration.py -v
```

## Troubleshooting

**"FRED_API_KEY environment variable is not set"**
Ensure the `FRED_API_KEY` is passed in your MCP configuration's `env` block, or set it in your shell environment.

**Rate limiting**
The server limits requests to 120 per minute (matching FRED API limits). If you hit the limit, requests will automatically wait — no action needed.

**Verifying the server is running**
```bash
claude mcp list
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

MIT
