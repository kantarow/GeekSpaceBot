from discord.ext import commands
from gsbot import GSBot
from datetime import timedelta

import re
import discord


class GenEmbed(commands.Cog):
    def __init__(self, bot: GSBot):
        self.bot = bot
        self.urlregex = re.compile(
            r"(https?:\/\/(?:|ptb\.|canary\.)discordapp\.com\/channels\/[0-9]{18,19}\/[0-9]{18,19}\/[0-9]{18,19})"
        )
        self.idregex = re.compile(r"[0-9]{18,19}")

    @commands.Cog.listener()
    async def on_message(self, message):
        urls = self.urlregex.findall(message.content)

        if len(urls) < 1:
            return

        for url in urls:
            embed = await self.generate_embed_from_url(url)
            await message.channel.send(embed=embed)

    async def generate_embed_from_url(self, url) -> discord.Embed:
        """DiscordのメッセージURLからEmbedオブジェクトを生成して返します。

        :param url: Embedを生成したいメッセージのURL。
        :type url: str
        :return: Discordのメッセージから生成したEmbedオブジェクト。
        :rtype: discord.Embed
        """
        ids = self.idregex.findall(url)  # [GuildID, ChannelID, MessageID]
        channel = await self.bot.fetch_channel(ids[1])
        message = await channel.fetch_message(ids[2])

        embed = discord.Embed()
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.description = message.content

        if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)

        timestamp = (message.created_at + timedelta(hours=9)).strftime(
            "%Y/%m/%d %H:%M:%S"
        )
        embed.set_footer(
            text="{0} - {1} | {2}".format(message.guild.name, channel.name, timestamp)
        )

        return embed


def setup(bot: GSBot):
    bot.add_cog(GenEmbed(bot))
