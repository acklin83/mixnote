"""Shared rate limiter.

Defined in its own module so both main.py (wiring) and the routers
(decorators) can import the same Limiter instance.
"""
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request


def _client_ip(request: Request) -> str:
    """Prefer the real client IP behind a reverse proxy (nginx/Caddy set
    X-Forwarded-For), falling back to the direct peer address."""
    xff = request.headers.get("x-forwarded-for")
    if xff:
        return xff.split(",")[0].strip()
    return get_remote_address(request)


limiter = Limiter(key_func=_client_ip)
