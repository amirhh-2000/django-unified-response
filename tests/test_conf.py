import pytest

from django_unified_response.conf import DEFAULTS, DURSettings


def test_defaults():
    conf = DURSettings({}, DEFAULTS)
    assert conf.ENABLE is True
    assert conf.CAMELCASE_KEYS is False
    from django_unified_response.formatters import DefaultFormatter

    assert conf.FORMATTER_CLASS == DefaultFormatter


def test_user_override():
    conf = DURSettings({"ENABLE": False, "CAMELCASE_KEYS": True}, DEFAULTS)
    assert conf.ENABLE is False
    assert conf.CAMELCASE_KEYS is True


def test_invalid_key_raises():
    with pytest.raises(RuntimeError):
        DURSettings({"INVALID_KEY": True}, DEFAULTS)


def test_caching():
    conf = DURSettings({"ENABLE": False}, DEFAULTS)
    first = conf.ENABLE
    conf._user_settings["ENABLE"] = True
    second = conf.ENABLE
    assert first == second


def test_reload():
    conf = DURSettings({"ENABLE": False}, DEFAULTS)
    assert conf.ENABLE is False
    conf._user_settings["ENABLE"] = True
    conf.reload()
    assert conf.ENABLE is True
