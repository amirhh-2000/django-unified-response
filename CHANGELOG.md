# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - Unreleased

### BREAKING CHANGES

- **Response format** changed from `{"status": "success"/"error"}` to a
  richer structure: `{"success": true/false, "data/error": ...}`.
- **Settings** are now nested under `DUR_SETTINGS` (instead of top‑level
  `UNIFIED_RESPONSE_*` keys).
- **Formatter API** now requires a class that inherits from
  `BaseFormatter` with separate `format_success`, `format_fail`,
  `format_error` methods.
- **Exception classes** re‑architected around `BaseAPIException` with
  `message`, `code`, `details` attributes.

### Added

- `conf.py`: zero‑configuration with lazy loading, caching, and automatic
  reload on `setting_changed`.
- `handlers.py`: robust exception handler that parses every DRF error shape.
- `renderers.py`: smart extraction of `data`/`meta`, prevention of
  double‑wrapping, and detection of paginated responses.
- Optional Swagger/OpenAPI support via `drf‑spectacular` soft dependency
  (`UnifiedResponseAutoSchema`).
- `@bypass_unified_response` decorator for per‑view bypass.
- `CAMELCASE_KEYS` option to recursively camelCase response keys.
- Validation of `DUR_SETTINGS` keys raises immediate error on misconfiguration.
- `extract_paginated_data` now supports `CursorPagination` and other
  non‑count paginators.

### Fixed

- `UnifiedJSONRenderer` no longer nests payloads when `data` and `meta` are
  present in custom responses.
- Bypass attribute name aligned between decorator (`_bypass_unified_response`)
  and schema detection.
- Pagination detection widened to recognise any DRF response containing
  `"results"`.

### Removed

- Unused `CUSTOM_ERROR_CODES` setting (was never implemented).
- Unused `BYPASS_URLS` setting (bypass is now controlled exclusively via
  the decorator or `_bypass_unified_response` attribute).

---

## [0.1.0] - 2025-08-XX

### Added

- Initial release of django-unified-response.
- Unified success response format with `{"status": "success", "data": ...}`.
- Unified error response format with `{"status": "error", ...}`.
- Custom exceptions for common API scenarios.
- Pluggable response formatter.
- Support for Django 3.2–4.2, Python 3.8–3.11.
- PyPI publication.
