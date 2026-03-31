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
    if isinstance(data, dict) and "results" in data and "count" in data:
        data_copy = data.copy()

        actual_data = data_copy.pop("results")
        actual_meta = {
            "pagination": {
                "count": data_copy.get("count"),
                "next": data_copy.get("next"),
                "previous": data_copy.get("previous"),
            }
        }
        return actual_data, actual_meta

    return None, None
