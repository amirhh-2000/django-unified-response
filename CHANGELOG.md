# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0](https://github.com/amirhh-2000/django-unified-response/compare/v0.1.0...v0.2.0) (2026-05-21)


### Features

* add `[@bypass](https://github.com/bypass)_unified_response` decorator for opt-out capability ([a4e8ccf](https://github.com/amirhh-2000/django-unified-response/commit/a4e8ccf4fd8c23780a1856cf9c39924f698631c7))
* add automatic pagination extraction to unified renderer ([fd6a400](https://github.com/amirhh-2000/django-unified-response/commit/fd6a40095ada21850f1dac33257b95b95eb49795))
* Add CI and Changelog update workflows ([0e66d84](https://github.com/amirhh-2000/django-unified-response/commit/0e66d846fc2774f509eb6891c630ec0f0b5d0739))
* Add makefile and configure project metadata ([5904897](https://github.com/amirhh-2000/django-unified-response/commit/590489721afa46d51b83d4b1ddc4b2037617004d))
* add swagger ([be2ccf4](https://github.com/amirhh-2000/django-unified-response/commit/be2ccf4954b07263491e4be346856610ca232359))
* apply camelCase transform to error responses ([41fdea2](https://github.com/amirhh-2000/django-unified-response/commit/41fdea24e5d5a3959e81feed7f46a9be5af02c15))
* enhance pagination detection to support more DRF paginators ([e9b68b0](https://github.com/amirhh-2000/django-unified-response/commit/e9b68b06175fcd0b81cb6ac44c67d853119093b7))
* implement core unified response components ([5b9c31a](https://github.com/amirhh-2000/django-unified-response/commit/5b9c31ab667690175166f044919f881f3951876a))


### Bug Fixes

* align bypass attribute name in schema with decorator ([5e776ac](https://github.com/amirhh-2000/django-unified-response/commit/5e776ace42462ad4a1d6d56e694cb4f1f46a5c0d))
* correct bandit path and remove safety from CI ([ca5bc3a](https://github.com/amirhh-2000/django-unified-response/commit/ca5bc3a621e90ee291078aa26235e7b13271881c))
* correct context references in changelog workflow ([c531355](https://github.com/amirhh-2000/django-unified-response/commit/c53135546775387df896d8f3e64c5df2fd1f1f8f))
* correct tab indentation in Makefile ([8d9755a](https://github.com/amirhh-2000/django-unified-response/commit/8d9755a014af8a9434faaeab806dcdbf5870206a))
* exclude test_project from ruff and remove safety from CI ([b34e5b6](https://github.com/amirhh-2000/django-unified-response/commit/b34e5b6be4b333f842e221e1c2dacbb02268682f))
* handle non-API exceptions by generating a 500 response ([171f48a](https://github.com/amirhh-2000/django-unified-response/commit/171f48a797493f0733e31bd48746dc1b45e27ffc))
* **renderers:** smart extraction of meta to prevent nesting inside data ([b271e00](https://github.com/amirhh-2000/django-unified-response/commit/b271e00761525f72d35a390b9d62adafc2ae1155))
* replace google-release-please with old file ([60c194f](https://github.com/amirhh-2000/django-unified-response/commit/60c194f9960ca307413f499478dd6c7d06a9965f))
* restructure changelog workflow ([77fd45b](https://github.com/amirhh-2000/django-unified-response/commit/77fd45bf13ea035fd109041d3bcd9109cd18549b))
* triggers on tags ([1fc80e1](https://github.com/amirhh-2000/django-unified-response/commit/1fc80e16e1b20f434752fb4a949a8797b89c36eb))
* validate user settings on load instead of only in constructor ([c1e646a](https://github.com/amirhh-2000/django-unified-response/commit/c1e646a2ebd3086ea9e0e42ea71ecb9d8e15de4b))


### Documentation

* add clarifying comment for meta/data extraction logic ([9c3364b](https://github.com/amirhh-2000/django-unified-response/commit/9c3364be8dc953990e459d0ce5b6571c4dcfece8))
* **changelog:** update unreleased section with core features and bug ([85dda9d](https://github.com/amirhh-2000/django-unified-response/commit/85dda9d6838beb922adf0a71129cba9df7d0a019))
* update Django support badge to include version 5.0 ([2011ee1](https://github.com/amirhh-2000/django-unified-response/commit/2011ee1330f70b3156bab481b1acfb7662b6c2d4))

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
