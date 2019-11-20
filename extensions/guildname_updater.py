from discord.ext import commands, tasks
from gsbot import GSBot


class GuildNameUpdater(commands.Cog):
    def __init__(self, bot: GSBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != 406357894427312148:
            return

        self.change_guild_name()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id != 406357894427312148:
            return

        self.change_guild_name()

    def change_guild_name(self):
        guild = self.bot.get_guild(406357894427312148)
        await guild.edit(name="Geek-Space +{0} members".format(guild.member_count))


def setup(bot):
    bot.add_cog(GuildNameUpdater(bot))
