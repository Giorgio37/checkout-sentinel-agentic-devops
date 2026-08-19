from __future__ import annotations

from dataclasses import dataclass

from .telemetry import span


@dataclass(frozen=True)
class CheckoutResponse:
    subtotal: float
    shipping: float
    total: float
    version: str


def checkout(subtotal: float, free_shipping_threshold: float, version: str = "2.3.1") -> CheckoutResponse:
    with span(
        "checkout POST /checkout",
        {
            "service.name": "checkout-api",
            "http.request.method": "POST",
            "http.route": "/checkout",
            "service.version": version,
        },
    ):
        if subtotal < 0:
            raise ValueError("subtotal must be non-negative")
        shipping = 0.0 if subtotal >= free_shipping_threshold else 7.99
        return CheckoutResponse(subtotal, shipping, round(subtotal + shipping, 2), version)

