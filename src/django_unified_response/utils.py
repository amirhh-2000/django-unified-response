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
