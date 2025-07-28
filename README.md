# Django Unified Response

A reusable Django app that provides standardized, consistent, and customizable JSON responses for your Django REST Framework APIs.

## Features

* **Unified Success Response:** All successful responses are wrapped in a consistent `{"status": "success", "data": ...}` structure.
* **Unified Error Response:** All exceptions (validation, authentication, custom errors, etc.) are caught and returned in a consistent `{"status": "error", "message": ..., "error_code": ...}` structure.
* **Custom Exceptions:** Ships with a set of clear, high-level exceptions (`NotFoundException`, `IntegrityException`, etc.) for common API scenarios.
* **Pluggable & Customizable:** Don't like the default format? You can provide your own formatter class to define a project-wide custom response structure.
* **Metadata Support:** Easily pass extra metadata (e.g., pagination, request IDs) in your responses via a `meta` key.

## Installation

Install the package from PyPI:

```bash
pip install django-unified-response
````

Or, if you are developing locally, navigate to the project root and install in editable mode:

```bash
pip install -e .
```

## Quick Start & Configuration

1.  Ensure `rest_framework` is in your `INSTALLED_APPS` in `settings.py`. You do **not** need to add `django_unified_response` to `INSTALLED_APPS` as it doesn't contain any models or template tags.

2.  Configure Django REST Framework in your `settings.py` to use the custom exception handler and renderer.

    ```python
    # settings.py

    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': [
            'django_unified_response.renderers.UnifiedJSONRenderer',
            # Add BrowsableAPIRenderer if you want to use the DRF web interface for testing
            'rest_framework.renderers.BrowsableAPIRenderer',
        ],
        'EXCEPTION_HANDLER': 'django_unified_response.handlers.custom_exception_handler',
    }
    ```

## How to Use

### Success Responses

Your views will now automatically return formatted success responses. You just need to return a standard DRF `Response` object.

```python
# in your views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class MyView(APIView):
    def get(self, request):
        payload = {"id": 1, "name": "Test Item"}
        return Response(payload)
```

The client will receive:

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

To include metadata, add a `meta` key to your response dictionary. The renderer will automatically separate it.

```python
# in your views.py
def get(self, request):
    payload = {
        "items": [{"id": 1}, {"id": 2}],
        "meta": {"pagination": {"count": 2, "page": 1}}
    }
    return Response(payload)
```

### Error Responses

#### Using Standard DRF Exceptions

The library will automatically catch and format default DRF exceptions. For example, using a serializer:

```python
# in your views.py
def post(self, request):
    serializer = MySerializer(data=request.data)
    # This will raise a DRF ValidationError, which our handler will format
    serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=201)
```

The client will receive a formatted `validation_error`:

```json
{
    "status": "error",
    "message": "Input validation failed.",
    "error_code": "validation_error",
    "errors": {
        "email": [ "Enter a valid email address." ]
    },
    "meta": {}
}
```

#### Using Custom Library Exceptions

For more specific business logic errors, import and raise the custom exceptions from the library.

```python
# in your views.py
from django_unified_response.exceptions import NotFoundException, IntegrityException
from django.db import IntegrityError
from my_app.models import Product

def get_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise NotFoundException() # Returns a formatted 404

def create_product(request):
    try:
        # ... logic to create product ...
    except IntegrityError:
        # Returns a formatted 409 Conflict
        raise IntegrityException("A product with this SKU already exists.")
```

## Advanced Customization

If the default response structure doesn't fit your needs, you can define your own global response format. The library is designed to be flexible, just like Django itself.

1.  **Create a new formatter class** anywhere in your Django project. It should inherit from `django_unified_response.formatters.DefaultResponseFormatter`. You only need to override the methods you want to change.

    For example, if you only want to change the error format but keep the success format the same, you can do this:

    ```python
    # my_app/formatters.py
    from django_unified_response.formatters import DefaultResponseFormatter

    class CustomResponseFormatter(DefaultResponseFormatter):
        # The format_success method is inherited and works as before.
        # We only override format_error.
        def format_error(self, message, error_code, errors=None, status_code=400, meta=None):
            return {
                "ok": False,
                "error": {
                    "code": error_code,
                    "message": message,
                    "details": errors
                },
                "meta": meta or {}
            }
    ```

2.  **Update your `settings.py`** to point to your new class:

    ```python
    # settings.py

    # Point to your custom formatter class
    UNIFIED_RESPONSE_FORMATTER_CLASS = 'my_app.formatters.CustomResponseFormatter'
    ```

That's it\! Your project will now use your custom error format while still using the library's default success format.

## Contributing
Contributions are welcome! If you have a feature request, bug report, or want to improve the library, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make your changes and add tests to cover them.
4. Ensure all tests pass by running them from the test_project directory.
5. Submit a pull request with a clear description of your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
