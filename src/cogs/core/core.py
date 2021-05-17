from datetime import datetime
from os import getenv

from discord import Message, RawMessageDeleteEvent
from discord.ext import commands

from src.internal.bot import Bot


class Core(commands.Cog):
    """Core metric collection."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def is_staff(member) -> bool:
        return int(getenv("STAFF")) in member._roles

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not message.guild: return

        QUERY = "INSERT INTO Messages Values ($1, $2, $3, $4, $5, $6, $7, $8);"

        await self.bot.db.execute(
            QUERY,
            message.id,
            message.channel.id,
            message.channel.category.id if message.channel.category else None,
            message.guild.id,
            message.author.id,
            self.is_staff(message.author),
            message.author.bot,
            message.created_at,
        )

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload: RawMessageDeleteEvent) -> None:
        if not payload.guild_id: return

        QUERY = "INSERT INTO DeletedMessages VALUES ($1, $2);"

        await self.bot.db.execute(
            QUERY,
            payload.message_id,
            datetime.utcnow(),
        )

    @commands.command(name="stats")
    @commands.is_owner()
    async def stats(self, ctx: commands.Context) -> None:
        M_QUERY = "SELECT COUNT(*) FROM Messages;"
        DM_QUERY = "SELECT COUNT(*) FROM DeletedMessages;"

        messages = await self.bot.db.fetchrow(M_QUERY)
        deleted = await self.bot.db.fetchrow(DM_QUERY)

        messages, deleted = messages[0], deleted[0]

        await ctx.send(f"Total messages: {messages}\nDeleted messages: {deleted}")


def setup(bot: Bot):
    bot.add_cog(Core(bot))
