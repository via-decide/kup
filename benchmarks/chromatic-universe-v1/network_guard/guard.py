from __future__ import annotations

import socket


class NetworkAccessDenied(RuntimeError):
    pass


def _blocked(*_args, **_kwargs):
    raise NetworkAccessDenied("network access is disabled for KUP benchmark execution")


def install() -> None:
    """Fail closed on Python socket entry points used by normal networking libraries."""
    socket.socket = _blocked  # type: ignore[assignment]
    socket.create_connection = _blocked  # type: ignore[assignment]
    socket.socketpair = _blocked  # type: ignore[assignment]
