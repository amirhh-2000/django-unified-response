# Django Unified Response

A reusable Django app that standardizes JSON responses for Django REST Framework APIs, ensuring consistency and customization.

## ✨ Features

- **Unified Success Response**: Wraps all successful responses in a consistent `{"status": "success", "data": ...}` structure.
- **Unified Error Response**: Catches and formats exceptions (validation, authentication, etc.) into a standard `{"status": "error", "message": ..., "error_code": ...}` structure.
- **Custom Exceptions**: Includes high-level exceptions like `NotFoundException` and `IntegrityException` for common API scenarios.
- **Pluggable & Customizable**: Define a project-wide custom response structure with your own formatter class.
- **Metadata Support**: Add extra metadata (e.g., pagination, request IDs) via a `meta` key.

## 📦 Installation

Install the package from PyPI:

```bash
pip install django-unified-response
```

For local development, navigate to the project root and install in editable mode:

```bash
pip install -e .
```

## 🚀 Quick Start & Configuration

1. Ensure `rest_framework` is in your `INSTALLED_APPS` in `settings.py`. No need to add `django_unified_response` as it contains no models or template tags.

2. Configure Django REST Framework in `settings.py` to use the custom exception handler and renderer:

   ```python
   # settings.py
   REST_FRAMEWORK = {
       'DEFAULT_RENDERER_CLASSES': [
           'django_unified_response.renderers.UnifiedJSONRenderer',
           # Optional: Include for DRF's browsable API
           'rest_framework.renderers.BrowsableAPIRenderer',
       ],
       'EXCEPTION_HANDLER': 'django_unified_response.handlers.custom_exception_handler',
   }
   ```

## 🛠️ Usage

### Success Responses

Return a standard DRF `Response` object, and the library formats it automatically:

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class MyView(APIView):
    def get(self, request):
        payload = {"id": 1, "name": "Test Item"}
        return Response(payload)
```

**Output**:

```json
{
  "status": "success",
  "message": "Success",
  "data": {
    "id": 1,
    "name": "Test Item"
  },
  "meta": {}
}
```

To include metadata, add a `meta` key:

```python
# views.py
def get(self, request):
    payload = {
        "items": [{"id": 1}, {"id": 2}],
        "meta": {"pagination": {"count": 2, "page": 1}}
    }
    return Response(payload)
```

**Output**:

```json
{
  "status": "success",
  "message": "Success",
  "data": {
    "items": [{ "id": 1 }, { "id": 2 }]
  },
  "meta": {
    "pagination": { "count": 2, "page": 1 }
  }
}
```

### Error Responses

#### Standard DRF Exceptions

The library formats DRF exceptions automatically:

```python
# views.py
def post(self, request):
    serializer = MySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=201)
```

**Output** (on validation failure):

```json
{
  "status": "error",
  "message": "Input validation failed.",
  "error_code": "validation_error",
  "errors": {
    "email": ["Enter a valid email address."]
  },
  "meta": {}
}
```

#### Custom Library Exceptions

Use built-in exceptions for specific errors:

```python
# views.py
from django_unified_response.exceptions import NotFoundException, IntegrityException
from django.db import IntegrityError
from my_app.models import Product

def get_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise NotFoundException()  # Returns 404

def create_product(request):
    try:
        # ... create product logic ...
    except IntegrityError:
        raise IntegrityException("A product with this SKU already exists.")  # Returns 409
```

## ⚙️ Advanced Customization

Customize the response structure by creating a formatter class:

1. **Create a formatter class** with `format_success` and `format_error` methods:

   ```python
   # my_app/formatters.py
   class CustomResponseFormatter:
       @staticmethod
       def format_success(data, status_code=200, message="OK", meta=None):
           return {"ok": True, "result": data, "meta": meta or {}}

       @staticmethod
       def format_error(message, error_code, errors=None, status_code=400, meta=None):
           return {"ok": False, "error": {"code": error_code, "message": message, "details": errors}, "meta": meta or {}}
   ```

2. **Update `settings.py`** to use the custom formatter:

   ```python
   # settings.py
   UNIFIED_RESPONSE_FORMATTER_CLASS = 'my_app.formatters.CustomResponseFormatter'
   ```

All responses will now use your custom structure.

## 📚 Notes

- Ensure compatibility with Django REST Framework versions in your project.
- Test custom formatters thoroughly to avoid breaking response consistency.
