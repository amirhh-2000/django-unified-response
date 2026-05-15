def to_camel_case(snake_str):
    """
    Converts a snake_case string to camelCase.
    """

    components = snake_str.split("_")

    return components[0] + "".join(x.title() for x in components[1:])


def camelize_keys(data):
    """
    Recursively converts all dictionary keys from snake_case to camelCase.
    """

    if isinstance(data, dict):
        return {to_camel_case(k): camelize_keys(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [camelize_keys(item) for item in data]
    return data


def extract_paginated_data(data):
    """
    Detects paginated DRF responses and extracts 'results' and metadata.

    Handles both standard PageNumberPagination (has 'count') and
    other pagination styles like CursorPagination (no 'count').
    """
    if isinstance(data, dict) and "results" in data:
        data_copy = data.copy()
        results = data_copy.pop("results", None)

        meta = {"pagination": {}}
        # Common pagination fields
        for field in ("count", "next", "previous", "cursor"):
            if field in data_copy:
                meta["pagination"][field] = data_copy.pop(field)

        # Any remaining top-level keys that are not 'results' are kept
        # as extra metadata (e.g., custom pagination info).
        if data_copy:
            meta["pagination"].update(data_copy)

        return results, meta

    return None, None
