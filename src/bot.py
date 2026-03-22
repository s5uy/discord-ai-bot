from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import discord
from discord import app_commands

from src.config.logging_setup import configure_logging
from src.cogs import chat as chat_cog
from src.config.settings import ConfigError, Settings, load_settings
from src.services.llm import LlmService

log = logging.getLogger("bot")


class DiscordBot(discord.Client):
    def __init__(self, settings: Settings) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)
        self.settings = settings
        self.llm = LlmService(settings)

    async def setup_hook(self) -> None:
        chat_cog.register(self.tree, llm=self.llm, owner_display=self.settings.bot_owner)

        @self.tree.error
        async def on_app_command_error(
            interaction: discord.Interaction,
            error: app_commands.AppCommandError,
        ) -> None:
            log.exception("Slash command error")
            try:
                if interaction.response.is_done():
                    await interaction.followup.send(
                        "Something went wrong running this command.",
                        ephemeral=True,
                    )
                else:
                    await interaction.response.send_message(
                        "Something went wrong running this command.",
                        ephemeral=True,
                    )
            except discord.HTTPException:
                pass

        guild_id = self.settings.discord_guild_id
        if guild_id is not None:
            guild = discord.Object(id=guild_id)
            await self.tree.sync(guild=guild)
            log.info("Application commands synced to guild %s (instant updates)", guild_id)
        else:
            synced = await self.tree.sync()
            log.info("Application commands synced globally (%d commands)", len(synced))

    async def on_ready(self) -> None:
        assert self.user is not None
        log.info("Connected as %s (%s)", self.user, self.user.id)


async def main() -> None:
    configure_logging()
    try:
        settings = load_settings()
    except ConfigError as e:
        log.error("%s", e)
        raise SystemExit(1) from e
    bot = DiscordBot(settings)
    await bot.start(settings.discord_token)


if __name__ == "__main__":
    asyncio.run(main())
