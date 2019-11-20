from discord.ext import commands
from gsbot import GSBot
from datetime import timedelta

import re
import discord
import logging


logger = logging.getLogger("gsbot.quote")


class Quote(commands.Cog):
    def __init__(self, bot: GSBot):
        self.bot = bot
        self.urlregex = re.compile(
            r"(https?:\/\/(?:|ptb\.|canary\.)discordapp\.com\/channels\/[0-9]{18,19}\/[0-9]{18,19}\/[0-9]{18,19})"
        )
        self.idregex = re.compile(r"[0-9]{18,19}")
        logger.info("Quote Cog is initialized.")

    @commands.Cog.listener()
    async def on_message(self, message):
        urls = self.urlregex.findall(message.content)

        if len(urls) < 1:
            return

        for url in urls:
            embed = await self.generate_embed_from_url(url)
            await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        user = self.bot.get_user(payload.user_id)

        if user.bot:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if message.author != self.bot.user:
            return

        if payload.emoji.name == "❌":
            await message.delete()

    async def generate_embed_from_url(self, url: str) -> discord.Embed:
        """DiscordのメッセージURLからEmbedオブジェクトを生成して返します。

        :param url: Embedを生成したいメッセージのURL。
        :type url: str
        :return: Discordのメッセージから生成したEmbedオブジェクト。
        :rtype: discord.Embed
        """
        message = self.get_message_by_url_recursive(url)

        embed = discord.Embed()
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.description = message.content + "\n\n[元のメッセージ]({0})".format(url)

        if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)

        timestamp = (message.created_at + timedelta(hours=9)).strftime(
            "%Y/%m/%d %H:%M:%S"
        )
        embed.set_footer(
            text="{0} - {1} | {2}".format(message.guild.name, message.channel.name, timestamp)
        )

        return embed

    def get_message_by_url_recursive(self, url):
        message = self.get_message_by_url(url)

        if self.is_url_only(message):
            content = message.content
            message = self.get_message_by_url_recursive(content)

        return message

    def get_message_by_url(self, url: str):
        ids = self.idregex.findall(url)  # [GuildID, ChannelID, MessageID]
        channel = await self.bot.fetch_channel(ids[1])
        message = await channel.fetch_message(ids[2])

        return message

    def is_url_only(self, message: discord.Message):
        return self.urlregex.fullmatch(message.content) is not None


def setup(bot: GSBot):
    bot.add_cog(Quote(bot))
