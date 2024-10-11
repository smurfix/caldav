from __future__ import annotations

from httpx import Auth, Request, Response
import typing

class BearerAuth(Auth):
    """
    Allows the 'auth' argument to be passed as a (username, password) pair,
    and uses HTTP Basic authentication.
    """

    def __init__(self, token: str | bytes) -> None:
        self._auth_header = f"Bearer {token}"

    def auth_flow(self, request: Request) -> typing.Generator[Request, Response, None]:
        request.headers["Authorization"] = self._auth_header
        yield request
