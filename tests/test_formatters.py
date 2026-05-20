import pytest

from django_unified_response.formatters import BaseFormatter, DefaultFormatter


def test_format_success():
    f = DefaultFormatter()
    result = f.format_success({"id": 1})
    assert result == {"success": True, "data": {"id": 1}, "meta": {}}


def test_format_fail():
    f = DefaultFormatter()
    result = f.format_fail("val_err", "Bad input", [{"field": "x"}])
    assert result["success"] is False
    assert result["error"]["type"] == "Fail"
    assert result["error"]["code"] == "val_err"
    assert result["error"]["details"] == [{"field": "x"}]


def test_format_error():
    f = DefaultFormatter()
    result = f.format_error("server_error", "Something wrong")
    assert result["success"] is False
    assert result["error"]["type"] == "Error"
    assert result["error"]["details"] is None


def test_base_formatter_not_implemented():
    bf = BaseFormatter()
    with pytest.raises(NotImplementedError):
        bf.format_success({})
    with pytest.raises(NotImplementedError):
        bf.format_fail("c", "m")
    with pytest.raises(NotImplementedError):
        bf.format_error("c", "m")
