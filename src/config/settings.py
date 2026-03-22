from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(_ROOT / ".env")


class ConfigError(ValueError):
    pass


def _env(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name)
    if v is None or v.strip() == "":
        return default
    return v.strip()


def _optional_int(name: str) -> int | None:
    raw = _env(name)
    if raw is None:
        return None
    try:
        return int(raw)
    except ValueError as e:
        raise ConfigError(f"{name} must be a valid integer") from e


def normalize_openai_base_url(url: str) -> str:
    u = url.strip().rstrip("/")
    path = urlparse(u).path or ""
    if path in ("", "/"):
        return f"{u}/v1"
    return u


@dataclass(frozen=True)
class Settings:
    discord_token: str
    openai_api_key: str
    openai_base_url: str | None
    openai_model: str
    system_prompt: str
    bot_owner: str | None
    discord_guild_id: int | None


def load_settings() -> Settings:
    token = _env("DISCORD_TOKEN")
    key = _env("OPENAI_API_KEY")
    if not token:
        raise ConfigError("DISCORD_TOKEN is required in .env")
    if not key:
        raise ConfigError("OPENAI_API_KEY is required in .env")
    base_raw = _env("OPENAI_BASE_URL")
    base = normalize_openai_base_url(base_raw) if base_raw else None
    model = _env("OPENAI_MODEL", "gpt-4o-mini") or "gpt-4o-mini"
    prompt = (
        _env(
            "SYSTEM_PROMPT",
            "You are a helpful assistant in a Discord server. Be clear and concise.",
        )
        or ""
    )
    return Settings(
        discord_token=token,
        openai_api_key=key,
        openai_base_url=base,
        openai_model=model,
        system_prompt=prompt,
        bot_owner=_env("BOT_OWNER"),
        discord_guild_id=_optional_int("DISCORD_GUILD_ID"),
    )
