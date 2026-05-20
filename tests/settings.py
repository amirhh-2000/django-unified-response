SECRET_KEY = "test"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "rest_framework",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
ROOT_URLCONF = "tests.urls"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "django_unified_response.renderers.UnifiedJSONRenderer",
        "rest_framework.renderers.JSONRenderer",
    ],
    "EXCEPTION_HANDLER": "django_unified_response.handlers.unified_exception_handler",
}
