from django_unified_response.decorators import bypass_unified_response


def test_bypass_sets_attribute():
    class FakeView:
        pass

    wrapped = bypass_unified_response(FakeView)
    assert wrapped._bypass_unified_response is True
