import discord

from discord.ext import commands
from gsbot import GSBot


CONFIGPATH = 'config/vcrole.json'


class VCRole(commands.Cog):
    def __init__(self, bot: GSBot):
        self.bot = bot
        self.config = bot.load_config(CONFIGPATH)

    @commands.group()
    async def vcrole(self, ctx):
        # TODO: リンクしたVCと役職のリストを表示
        pass

    @vcrole.command(name='add')
    async def add_vcrole(self, ctx, vc: discord.VoiceChannel, role: discord.Role):
        # TODO: VCと役職の紐付けを追加する
        setting = self.config.get(str(vc.id))
        if setting is None:
            setting = [role.id]
        else:
            setting.append(role.id)

        self.config[str(vc.id)] = setting
        self.bot.save_config(CONFIGPATH, self.config)

    @vcrole.command(name='remove')
    async def remove_vcrole(self, ctx, vc: discord.VoiceChannel, role: discord.Role):
        # TODO: VCと役職の紐付けを削除する
        setting = self.config.get(str(vc.id))

        if setting is None:
            await ctx.send('指定のボイスチャンネルには役職が設定されていません。')
            return

        try:
            setting.remove(role.id)
        except ValueError:
            await ctx.send('指定のボイスチャンネルには指定の役職が設定されていません。')
            return

        self.config[str(vc.id)] = setting
        self.bot.save_config(CONFIGPATH, self.config)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        pass


def setup(bot):
    bot.add_cog(VCRole(bot))
