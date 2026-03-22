<<<<<<< HEAD
# Discord × OpenAI bot

Minimal Discord bot: slash command `/ask` sends prompts to the OpenAI API. Configuration is environment-based so you can point at OpenAI’s hosted API or any compatible endpoint via `OPENAI_BASE_URL`.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).

## Setup

1. Python 3.10+

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and set at least `DISCORD_TOKEN` and `OPENAI_API_KEY`.

4. [Discord Developer Portal](https://discord.com/developers/applications): create an application, add a bot, copy the token into `.env`. Under **OAuth2 → URL Generator**, enable `bot` and `applications.commands`, pick scopes, invite the bot to your server.

5. Run from the project root (either form works):

   ```bash
   python -m src.bot
   python src/bot.py
   ```

## Environment

| Variable | Required | Description |
|----------|----------|-------------|
| `DISCORD_TOKEN` | yes | Bot token from the Discord application |
| `OPENAI_API_KEY` | yes | API key for the OpenAI-compatible endpoint |
| `OPENAI_BASE_URL` | no | OpenAI-compatible API base, usually ending in `/v1`. If you only set a host (no path), `/v1` is appended automatically. Omit entirely to use the SDK default |
| `OPENAI_MODEL` | no | Model id (default `gpt-4o-mini`) |
| `SYSTEM_PROMPT` | no | System message for the assistant |
| `BOT_OWNER` | no | Shown in `/about` |
| `DISCORD_GUILD_ID` | no | If set, slash commands sync to that guild only (fast while developing). Leave unset for global commands |
| `LOG_LEVEL` | no | Python logging level, e.g. `INFO`, `DEBUG` (default `INFO`) |

### Kiro / AWStore (`api.kiro.cheap`)

Use their API key and a Claude model id (not `gpt-4o-mini`). Base URL is usually `https://api.kiro.cheap/v1` or `https://api.kiro.cheap` (a `/v1` suffix is added when the URL has no path). See [their OpenAI-compatible docs](https://www.kiro.cheap/cheap-claude-api).

## Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Replace the copyright line in `LICENSE` with your name or organization before publishing if you want the notice to name you.

## Third-party

Uses [discord.py](https://github.com/Rapptz/discord.py) and the [OpenAI Python SDK](https://github.com/openai/openai-python); see their licenses in those repositories.
=======
# discord-ai-bot
Discord bot with slash commands, powered by the OpenAI-compatible API (/ask, configurable base URL and model).
>>>>>>> 0a91c157f216c54116c3049010db276ec442adf7
