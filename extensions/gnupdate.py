from discord.ext import commands, tasks
from gsbot import GSBot


class GuildNameUpdater(commands.Cog):
    def __init__(self, bot: GSBot):
        self.bot = bot
        self.name_update.start()

    def cog_unload(self):
        self.name_update.cancel()

    @tasks.loop(hours=1)
    async def name_update(self):
        guild = self.bot.get_guild(406357894427312148)
        await guild.edit(name='Geek-Space {0}'.format(guild.member_count))


def setup(bot):
    bot.add_cog(GuildNameUpdater(bot))
