import discord
import logging

from discord.ext import commands
from gsbot import GSBot


CONFIGPATH = 'config/vcrole.json'
logger = logging.getLogger('gsbot.vcrole')


class VCRole(commands.Cog):
    def __init__(self, bot: GSBot):
        self.bot = bot
        self.config = bot.load_config(CONFIGPATH)

    @commands.group()
    async def vcrole(self, ctx):
        # TODO: リンクしたVCと役職のリストを表示
        pass

    @vcrole.command(name='list')
    async def list_vcrole(self, ctx, vc: discord.VoiceChannel):
        settings = self.config.get(str(vc.id))

        if settings is None:
            await ctx.send('指定のボイスチャンネルにリンクされている役職は存在しません。')
            return

        embeds = list()
        embed = discord.Embed()
        count = 1
        for data in settings:
            guild = self.bot.get_guild(data['guild_id'])
            role = guild.get_role(data['role_id'])

            embed.add_field(
                name=str(count),
                value='Guild: {0}\nRole: {1}'.format(guild.name, role.name),
                inline=False,
            )

            count += 1

            # フィールドの数が20個になったら、新しいEmbedを作成する。
            if count % 20 == 0:
                embeds.append(embed)
                embed = discord.Embed()
        else:
            embeds.append(embed)

        for embed in embeds:
            await ctx.send(embed=embed)

    @vcrole.command(name='add')
    async def add_vcrole(self, ctx, vc: discord.VoiceChannel, role: discord.Role):
        settings = self.config.get(str(vc.id))
        if settings is None:
            settings = list()

            data = dict()
            data['role_id'] = role.id
            data['guild_id'] = role.guild.id

            settings.append(data)
        else:
            data = dict()
            data['role_id'] = role.id
            data['guild_id'] = role.guild.id

            settings.append(data)

        self.config[str(vc.id)] = settings
        self.bot.save_config(CONFIGPATH, self.config)

    @vcrole.command(name='remove')
    async def remove_vcrole(self, ctx, vc: discord.VoiceChannel, index: int):
        settings = self.config.get(str(vc.id))

        if settings is None:
            await ctx.send('指定のボイスチャンネルには役職が設定されていません。')
            return

        try:
            settings.pop(index - 1)
        except IndexError:
            await ctx.send('指定されたインデックスは範囲を超えています。')
            return

        self.config[str(vc.id)] = settings
        self.bot.save_config(CONFIGPATH, self.config)

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        # VCへの接続・切断以外を破棄
        if before.channel == after.channel:
            return
        if before.channel is None:
            await self.check_and_add_roles(member, after.channel)
            return
        elif after.channel is None:
            await self.check_and_remove_roles(member, before.channel)
            return

        await self.check_and_remove_roles(member, before.channel)
        await self.check_and_add_roles(member, after.channel)

    # HACK: check_and_remove_rolesと被る部分が多い。名称も不明瞭。要リファクタリング。
    async def check_and_add_roles(
        self, member: discord.Member, channel: discord.VoiceChannel
    ):
        settings = self.config.get(str(channel.id))

        if settings is None:
            return

        for data in settings:
            guild = self.bot.get_guild(data['guild_id'])
            if guild is None:
                logger.warning('Guild is not found. ID: {0}'.format(data['guild_id']))
                continue

            role = guild.get_role(data['role_id'])
            if role is None:
                logger.warning('Role is not found. ID: {0}'.format(data['role_id']))
                continue

            target_member = guild.get_member(member.id)
            if target_member is None:
                logger.info('Member is not joined to Guild. ID: {0}'.format(member.id))
            await target_member.add_roles(role)

    # HACK: check_and_add_rolesと被る部分が多い。名称も不明瞭。要リファクタリング。
    async def check_and_remove_roles(
        self, member: discord.Member, channel: discord.VoiceChannel
    ):
        settings = self.config.get(str(channel.id))

        if settings is None:
            return

        for data in settings:
            guild = self.bot.get_guild(data['guild_id'])

            if guild is None:
                logger.warning('Guild is not found. ID: {0}'.format(data['guild_id']))
                continue

            role = guild.get_role(data['role_id'])
            if role is None:
                logger.warning('Role is not found. ID: {0}'.format(data['role_id']))
                continue

            target_member = guild.get_member(member.id)
            if target_member is None:
                logger.info('Member is not joined to Guild. ID: {0}'.format(member.id))
            await target_member.remove_roles(role)


def setup(bot):
    bot.add_cog(VCRole(bot))
