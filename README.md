# fred-mcp

An MCP (Model Context Protocol) server that provides access to the full [FRED API](https://fred.stlouisfed.org/docs/api/fred/) (Federal Reserve Economic Data). Use it to search, explore, and retrieve economic data directly within Claude conversations.

## Features

- **29 tools** covering all FRED API endpoints (series, categories, releases, sources, tags)
- Full parameter support — no artificial limits on pagination or filtering
- Built-in rate limiting (120 requests/minute)
- Async HTTP client for efficient request handling

## Requirements

- Python 3.10+
- A free [FRED API key](https://fred.stlouisfed.org/docs/api/api_key.html)

## Installation

```bash
git clone https://github.com/floriancaro/fred-mcp.git
cd fred-mcp
pip install -e .
```

## Configuration

### Claude Code

Add to your MCP config (`~/.claude/.mcp.json` for global, or `.mcp.json` in your project root):

```json
{
  "mcpServers": {
    "fred": {
      "command": "python",
      "args": ["-m", "fred_mcp"],
      "cwd": "/path/to/fred-mcp",
      "env": {
        "FRED_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

A `.mcp.json.example` file is included in the repo — copy it and fill in your key.

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "fred": {
      "command": "python",
      "args": ["-m", "fred_mcp"],
      "cwd": "/path/to/fred-mcp",
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

## Development

```bash
pip install -e ".[dev]"

# Run unit tests
python -m pytest tests/test_client.py -v

# Run integration tests (requires FRED_API_KEY)
FRED_API_KEY=your-key python -m pytest tests/test_integration.py -v
```

## License

MIT
