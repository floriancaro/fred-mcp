# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-04-04

### Added

- 4 FRED Maps API tools: geofred_series_group, geofred_series_data, geofred_regional_data, geofred_shapes
- Literal type constraints for `order_by`, `tag_group_id`, `output_type`, and `filter_value` parameters
- Parameter docstrings for LLM-facing tool descriptions
- Server-level `instructions` for LLM client guidance
- Example prompts and troubleshooting sections in README
- GitHub Actions publish workflow with PyPI trusted publishing
- Dockerfile for container-based deployment
- Python 3.13 to CI test matrix

### Fixed

- Lifespan teardown no longer creates a client unnecessarily on shutdown
- HTTP 4xx error responses now include FRED API error details

## [0.1.0] - 2026-04-03

### Added

- 29 MCP tools covering the full FRED API (series, categories, releases, sources, tags)
- Async HTTP client with built-in rate limiting (120 requests/minute)
- Automatic API key injection and parameter sanitization
- Unit tests with mocked HTTP and integration tests against live API
- GitHub Actions CI for Python 3.10-3.12

[Unreleased]: https://github.com/floriancaro/fred-mcp-server/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/floriancaro/fred-mcp-server/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/floriancaro/fred-mcp-server/releases/tag/v0.1.0
