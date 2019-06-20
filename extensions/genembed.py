from discord.ext import commands
from gsbot import GSBot


class GenEmbed(commands.Bot):
    def __init__(self, bot: GSBot):
        self.bot = bot


def setup(bot: GSBot):
    bot.add_cog(GenEmbed(bot))
