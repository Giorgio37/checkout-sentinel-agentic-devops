import pytest

from checkout_sentinel.service import checkout


def test_shipping_threshold_boundary():
    assert checkout(49.99, 50.0).shipping == 7.99
    assert checkout(50.00, 50.0).shipping == 0.0


def test_negative_subtotal_is_rejected():
    with pytest.raises(ValueError):
        checkout(-1, 50.0)

