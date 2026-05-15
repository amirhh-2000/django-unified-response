from django.conf import settings
from django.core.signals import setting_changed
from django.utils.module_loading import import_string

DEFAULTS = {
    "ENABLE": True,
    "FORMATTER_CLASS": "django_unified_response.formatters.DefaultFormatter",
    "CAMELCASE_KEYS": False,
    "CUSTOM_ERROR_CODES": {},
    "BYPASS_URLS": [],
}

IMPORT_STRINGS = [
    "FORMATTER_CLASS",
]


class DURSettings:
    """
    Core settings manager for django-unified-response.
    Reads user settings from Django's settings.DUR_SETTINGS and falls back to DEFAULTS.
    """

    def __init__(self, user_settings=None, defaults=None, import_strings=None):
        if user_settings:
            self._user_settings = self.__check_user_settings(user_settings)
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            raw = getattr(settings, "DUR_SETTINGS", {})
            self._user_settings = self.__check_user_settings(raw)
        return self._user_settings

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(f"Invalid django-unified-response setting: '{attr}'")

        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]

        if attr in self.import_strings:
            val = import_string(val)

        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)
        self._cached_attrs.clear()
        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")

    def __check_user_settings(self, user_settings):
        for setting in user_settings.keys():
            if setting not in DEFAULTS:
                raise RuntimeError(
                    f"You have an invalid setting '{setting}' in DUR_SETTINGS."
                )
        return user_settings


dur_settings = DURSettings(None, DEFAULTS, IMPORT_STRINGS)


def reload_dur_settings(*args, **kwargs):
    setting = kwargs.get("setting")
    if setting == "DUR_SETTINGS":
        dur_settings.reload()


setting_changed.connect(reload_dur_settings)
