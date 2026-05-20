from django_unified_response.utils import camelize_keys, extract_paginated_data


def test_camelize_simple():
    data = {"first_name": "Amir", "last_name": "Hossein"}
    assert camelize_keys(data) == {"firstName": "Amir", "lastName": "Hossein"}


def test_camelize_nested():
    data = {"user_info": {"first_name": "Amir"}}
    expected = {"userInfo": {"firstName": "Amir"}}
    assert camelize_keys(data) == expected


def test_extract_paginated_standard():
    data = {"count": 10, "next": "url", "previous": "url", "results": [1, 2]}
    results, meta = extract_paginated_data(data)
    assert results == [1, 2]
    assert meta["pagination"]["count"] == 10


def test_extract_cursor_pagination():
    data = {"next": "url", "results": [3, 4], "cursor": "abc"}
    results, meta = extract_paginated_data(data)
    assert results == [3, 4]
    assert meta["pagination"]["next"] == "url"
    assert meta["pagination"]["cursor"] == "abc"


def test_non_paginated():
    data = {"foo": "bar"}
    assert extract_paginated_data(data) == (None, None)


def test_camelize_single_word():
    assert camelize_keys({"success": True}) == {"success": True}
