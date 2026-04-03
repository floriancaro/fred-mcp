# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-04-03

### Added

- 29 MCP tools covering the full FRED API (series, categories, releases, sources, tags)
- Async HTTP client with built-in rate limiting (120 requests/minute)
- Automatic API key injection and parameter sanitization
- Unit tests with mocked HTTP and integration tests against live API
- GitHub Actions CI for Python 3.10-3.12
