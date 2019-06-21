from discord.ext import commands
from gsbot import GSBot

import re
import discord


class GenEmbed(commands.Bot):
    def __init__(self, bot: GSBot):
        self.bot = bot
        self.urlregex = re.compile(
            r'(https?:\/\/(?:|ptb\.|canary\.)discordapp\.com\/channels\/[0-9]{18,19}\/[0-9]{18,19}\/[0-9]{18,19})'
        )
        self.idregex = re.compile(r'[0-9]{18,19}')

    @commands.Cog.listener()
    async def on_message(self, message):
        urls = self.urlregex.findall(message.content)

        if len(urls) < 1:
            return

        for url in urls:
            ids = self.idregex.findall(url)
            guild = self.bot.fetch_guild(ids[0])
            channel = guild.get_channel(ids[1])
            message = channel.fetch_message(ids[2])

    def generate_embed_from_url(self, url) -> discord.Embed:
        ids = self.idregex.findall(url)  # [GuildID, ChannelID, MessageID]
        guild = self.bot.fetch_guild(ids[0])
        channel = guild.get_channel(ids[1])
        message = channel.fetch_message(ids[2])

        embed = discord.Embed()
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        embed.description = message.content

        if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)

        embed.set_footer(text='送信日: {0} | ID: {1}'.format())


def setup(bot: GSBot):
    bot.add_cog(GenEmbed(bot))
