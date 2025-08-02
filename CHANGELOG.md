# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial release preparation
- GitHub Actions CI/CD pipeline setup
- Code quality tools integration (ruff, pytest, bandit)
- Development workflow with Makefile and uv package manager

## [0.1.0] - 2024-01-XX

### Added

- Initial release of django-unified-response
- Unified success response format with `{"status": "success", "data": ...}` structure
- Unified error response format with `{"status": "error", "message": ..., "error_code": ...}` structure
- Custom exceptions: `NotFoundException`, `IntegrityException`, and others for common API scenarios
- Pluggable and customizable response formatters via `DefaultResponseFormatter`
- Metadata support for responses via `meta` key
- Support for Django 3.2, 4.0, 4.1, and 4.2
- Support for Python 3.8, 3.9, 3.10, and 3.11
- Comprehensive documentation and examples
- PyPI package publication
