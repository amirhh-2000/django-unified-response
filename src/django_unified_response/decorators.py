def bypass_unified_response(view_func_or_class):
    """
    Mark a view to bypass the unified response wrapper.
    The view's DRF response will be returned as-is without
    being processed by the unified response handler.
    """
    view_func_or_class._bypass_unified_response = True
    return view_func_or_class
