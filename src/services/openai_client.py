from __future__ import annotations

import os

from openai import AsyncOpenAI

from src.config.settings import Settings, normalize_openai_base_url


def resolve_openai_base_url(settings: Settings) -> str | None:
    raw = settings.openai_base_url or os.environ.get("OPENAI_BASE_URL")
    if not raw or not str(raw).strip():
        return None
    return normalize_openai_base_url(str(raw).strip())


def create_async_openai_client(settings: Settings) -> AsyncOpenAI:
    kwargs: dict = {"api_key": settings.openai_api_key}
    base = resolve_openai_base_url(settings)
    if base:
        kwargs["base_url"] = base
    return AsyncOpenAI(**kwargs)
