from __future__ import annotations

import logging

import discord
from discord import app_commands

from src.config.constants import ASK_PROMPT_MAX, DISCORD_MESSAGE_MAX
from src.services.llm import LlmRequestError, LlmService
from src.utils.text import chunk_discord

log = logging.getLogger(__name__)


def register(
    tree: app_commands.CommandTree,
    *,
    llm: LlmService,
    owner_display: str | None,
) -> None:
    @tree.command(name="ask", description="Send a message to the AI")
    @app_commands.describe(prompt="What you want to say to the model")
    async def ask(
        interaction: discord.Interaction,
        prompt: app_commands.Range[str, 1, ASK_PROMPT_MAX],
    ) -> None:
        await interaction.response.defer(thinking=True)
        try:
            text = await llm.reply(str(prompt))
        except LlmRequestError as e:
            await interaction.followup.send(e.public_message, ephemeral=True)
            return
        except Exception:
            log.exception("Unhandled error in /ask")
            await interaction.followup.send(
                "An unexpected error occurred. Try again later.",
                ephemeral=True,
            )
            return

        if not text:
            text = "*(No text in the model response.)*"

        parts = chunk_discord(text, DISCORD_MESSAGE_MAX)
        first, *rest = parts
        await interaction.followup.send(first)
        for chunk in rest:
            await interaction.followup.send(chunk)

    @tree.command(name="about", description="Bot info and credits")
    async def about(interaction: discord.Interaction) -> None:
        owner = owner_display or "Not set"
        embed = discord.Embed(
            title="Discord × OpenAI",
            description="Use `/ask` with your prompt. Configuration lives in `.env` (see `.env.example`).",
            color=discord.Color.blurple(),
        )
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Model", value=llm.model, inline=True)
        embed.add_field(name="API base", value=llm.api_base_url, inline=False)
        embed.set_footer(text="MIT License — see LICENSE in the repository")
        await interaction.response.send_message(embed=embed, ephemeral=True)
