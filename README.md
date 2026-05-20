# Django Unified Response

[![PyPI version](https://badge.fury.io/py/django-unified-response.svg)](https://badge.fury.io/py/django-unified-response)
[![Python Support](https://img.shields.io/pypi/pyversions/django-unified-response.svg)](https://pypi.org/project/django-unified-response/)
[![Django Support](https://img.shields.io/badge/Django-3.2%2C%204.2%2C%205.0-blue.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://github.com/amirhh-2000/django-unified-response/workflows/CI/badge.svg)](https://github.com/amirhh-2000/django-unified-response/actions)

> Wrap every Django REST Framework response in a clean, consistent, and fully customisable JSON envelope — no boilerplate, no weird edge cases.

---

## ✨ Why yet another response wrapper?

- **Zero boilerplate** – all views automatically get the same envelope.
- **DRF error‑proof** – the messiest validation errors are turned into a predictable, structured format.
- **Pagination‑aware** – detects standard, cursor, and custom paginators, keeping metadata tidy.
- **Swagger‑ready** – optional `drf-spectacular` integration generates the exact schemas.
- **Totally customisable** – replace the envelope globally by writing a formatter class, without touching the library.

---

## 📦 What responses look like

### ✅ Success

```json
{
    "success": true,
    "data": { "id": 1, "name": "Test Item" },
    "meta": {}
}
```

### ❌ Client error (4xx)

```json
{
    "success": false,
    "error": {
        "type": "Fail",
        "code": "validation_error",
        "message": "Input validation failed.",
        "details": [
            { "field": "email", "issue": "Enter a valid email address." }
        ]
    }
}
```

### 💥 Server error (5xx)

```json
{
    "success": false,
    "error": {
        "type": "Error",
        "code": "HTTP_500",
        "message": "A server error occurred.",
        "details": null
    }
}
```

---

## ⚙️ Requirements

- Python **3.10+**
- Django 3.2 / 4.0 / 4.1 / 4.2
- Django REST Framework 3.12+
- (Optional) `drf‑spectacular` for OpenAPI schema generation

---

## 🚀 Installation

```bash
pip install django-unified-response
```

### With Swagger support

```bash
pip install "django-unified-response[swagger]"
```

---

## 🛠 Quick Start

1. **No need to add to `INSTALLED_APPS`** – the package has no models.
2. Configure Django REST Framework in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'django_unified_response.renderers.UnifiedJSONRenderer',
        # Keep BrowsableAPIRenderer for the DRF web interface
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'EXCEPTION_HANDLER': 'django_unified_response.handlers.unified_exception_handler',
}
```

That’s it! Every response is now unified.

---

## 🔧 Configuration

All library settings live in the `DUR_SETTINGS` dictionary:

```python
# settings.py
DUR_SETTINGS = {
    # Formatter class that defines the envelope (default shown)
    "FORMATTER_CLASS": "django_unified_response.formatters.DefaultFormatter",
    # Convert snake_case keys to camelCase
    "CAMELCASE_KEYS": False,
    # Temporarily disable the entire wrapper
    "ENABLE": True,
}
```

| Setting           | Type                 | Default                                                 | Description                                            |
| ----------------- | -------------------- | ------------------------------------------------------- | ------------------------------------------------------ |
| `FORMATTER_CLASS` | string (import path) | `"django_unified_response.formatters.DefaultFormatter"` | Path to a formatter class (see Advanced Customisation) |
| `CAMELCASE_KEYS`  | bool                 | `False`                                                 | If `True`, all response keys become camelCase          |
| `ENABLE`          | bool                 | `True`                                                  | Set to `False` to return raw DRF responses globally    |

---

## 🧪 Usage

### Success responses

Return a standard DRF `Response`. The renderer wraps it automatically.

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class MyView(APIView):
    def get(self, request):
        return Response({"id": 1, "name": "Amir"})
```

**Client receives:**

```json
{
    "success": true,
    "data": { "id": 1, "name": "Amir" },
    "meta": {}
}
```

### Including metadata

If your response already has `"data"` and/or `"meta"` keys, the renderer respects them:

```python
return Response({
    "data": {"items": [...]},
    "meta": {"page": 1, "total": 42}
})
```

### Paginated responses

The renderer auto‑detects DRF pagination (any class that returns `"results"`), moves the results to `data`, and puts the rest (`count`, `next`, `previous`, `cursor`, etc.) under `meta.pagination`.

### Bypassing the wrapper

Use the decorator on any view to keep the raw DRF response:

```python
from django_unified_response.decorators import bypass_unified_response

@bypass_unified_response
class HealthCheckView(APIView):
    def get(self, request):
        return Response({"status": "ok"})
```

### Error responses

#### Standard DRF exceptions

Raised automatically by serializers — the handler formats them.

```python
serializer.is_valid(raise_exception=True)  # yields a formatted 4xx
```

#### Custom library exceptions

Import and raise for business‑logic errors:

```python
from django_unified_response.exceptions import (
    NotFoundException,
    IntegrityException,
    ValidationException,
    AuthenticationFailedException,
)

def get_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise NotFoundException()  # 404, code "not_found"

def create_product(request):
    try:
        ...
    except IntegrityError:
        raise IntegrityException(
            message="SKU already exists.",
            details={"sku": "duplicate"}
        )
```

---

## 📘 Swagger / OpenAPI

Install the `[swagger]` extra, then set the schema class:

```python
REST_FRAMEWORK = {
    # ...
    'DEFAULT_SCHEMA_CLASS': 'django_unified_response.schema.UnifiedResponseAutoSchema',
}
```

Your OpenAPI docs will automatically show the unified `success`/`error` shapes.

---

## 🎨 Advanced Customisation

You can replace the entire envelope by writing your own formatter.

1. Subclass `BaseFormatter` (or `DefaultFormatter` to override only parts):

```python
# my_app/formatters.py
from django_unified_response.formatters import BaseFormatter

class MyFormatter(BaseFormatter):
    def format_success(self, data, meta=None):
        return {"ok": True, "result": data, "extra": meta or {}}

    def format_fail(self, error_code, message, details=None):
        return {
            "ok": False,
            "problem": {
                "code": error_code,
                "what": message,
                "fields": details or [],
            },
        }

    def format_error(self, error_code, message, details=None):
        return {
            "ok": False,
            "problem": {
                "code": error_code,
                "what": "Internal error",
                "trace": message if settings.DEBUG else None,
            },
        }
```

2. Point to it in `DUR_SETTINGS`:

```python
DUR_SETTINGS = {
    "FORMATTER_CLASS": "my_app.formatters.MyFormatter",
}
```

Every response now follows your own contract.

---

## 👩‍💻 Development

### Prerequisites

- [uv](https://github.com/astral-sh/uv)
- Python 3.10+

### Setup

```bash
git clone https://github.com/amirhh-2000/django-unified-response.git
cd django-unified-response
make install-dev
```

### Commands

```bash
make install-dev   # install development deps
make test          # run tests
make lint          # ruff linter
make format        # ruff formatter
make security      # bandit security checks
make clean         # remove build artifacts
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes and write tests
4. Run `make lint` and `make test`
5. Update `CHANGELOG.md` (Keep a Changelog format)
6. Open a pull request

---

## 📄 Changelog

All notable changes are documented in [CHANGELOG.md](CHANGELOG.md).

---

## 📜 License

MIT. See [LICENSE](LICENSE).
