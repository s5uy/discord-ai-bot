from __future__ import annotations

import logging
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    OpenAIError,
    RateLimitError,
)

from src.config.settings import Settings
from src.services.openai_client import create_async_openai_client

log = logging.getLogger(__name__)


class LlmRequestError(Exception):
    def __init__(self, public_message: str) -> None:
        super().__init__(public_message)
        self.public_message = public_message


class LlmService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = create_async_openai_client(settings)
        self._model = settings.openai_model
        self._system = settings.system_prompt
        log.info("LLM client ready: base_url=%s model=%s", self._client.base_url, self._model)

    @property
    def model(self) -> str:
        return self._model

    @property
    def api_base_url(self) -> str:
        return str(self._client.base_url)

    async def reply(self, user_text: str) -> str:
        try:
            r = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": self._system},
                    {"role": "user", "content": user_text},
                ],
            )
        except RateLimitError as e:
            log.warning("OpenAI rate limit: %s", e)
            raise LlmRequestError("The model is busy — wait a few seconds and try again.") from e
        except AuthenticationError as e:
            log.error("OpenAI auth failed: %s", e)
            raise LlmRequestError("API authentication failed. Check `OPENAI_API_KEY` in `.env`.") from e
        except BadRequestError as e:
            log.warning("OpenAI bad request: %s", e)
            raise LlmRequestError(
                "The provider rejected the request (wrong model name or parameters)."
            ) from e
        except APIStatusError as e:
            log.warning("OpenAI HTTP error: %s", e)
            msg = _friendly_http_message(e)
            raise LlmRequestError(msg) from e
        except APIConnectionError as e:
            log.error("OpenAI connection error: %s", e)
            raise LlmRequestError("Could not reach the API. Check your network and base URL.") from e
        except APITimeoutError as e:
            log.warning("OpenAI timeout: %s", e)
            raise LlmRequestError("The request timed out — try again.") from e
        except OpenAIError as e:
            log.exception("OpenAI error: %s", e)
            raise LlmRequestError("Something went wrong talking to the model API.") from e

        choice = r.choices[0].message.content
        if not choice:
            return ""
        return choice.strip()


def _friendly_http_message(e: APIStatusError) -> str:
    code = getattr(e, "status_code", None)
    if code == 404:
        return "API route not found — check `OPENAI_BASE_URL` (usually must end with `/v1`)."
    if code == 401:
        return "API key rejected — verify `OPENAI_API_KEY` for this provider."
    if code == 403:
        return "Access denied — your key may not allow this model or endpoint."
    if code == 429:
        return "Rate limited — try again shortly."
    body = getattr(e, "body", None)
    if isinstance(body, dict) and (m := body.get("message")):
        return f"Provider error: {m}"
    return "The model API returned an error."
