from disnake import Member
from disnake.ext import commands
import json_reader
import time_events


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description='Замутить участника на сервере.')
    async def mute(self, interaction, user: Member, time: str = None):
        mute_role = json_reader.get_value(
            f'{interaction.guild.id}/config.json', 'mute_role')
        role = interaction.guild.get_role(mute_role)
        muted_users = json_reader.get_value(
            f'{interaction.guild.id}/mute_list.json', 'muted_users')
        is_muted = False
        for item in muted_users:
            if user.id in item:
                is_muted = True
        if not is_muted:
            try:
                if role:
                    end_time = time_events.get_end_time(time or '3650d')
                    muted_users.append(
                        [user.id, str(end_time)])
                    json_reader.set_value(
                        f'{interaction.guild.id}/mute_list.json', 'muted_users', muted_users)
                    await user.add_roles(role)
                    await interaction.response.send_message(f'{user.mention} был замучен', ephemeral=True)
                else:
                    await interaction.response.send_message('Роль `mute` не найдена на сервере. Добавьте ее с помощью команды /mute_role_set `@role`', ephemeral=True)
            except:
                await interaction.response.send_message(f'Произошла ошибка при муте {user.mention}.', ephemeral=True)
        else:
            await interaction.response.send_message(f'{user.mention} уже замучен.', ephemeral=True)

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description='Размутить участника на сервере.')
    async def unmute(self, interaction, user: Member):
        mute_role = json_reader.get_value(
            f'{interaction.guild.id}/config.json', 'mute_role')
        role = interaction.guild.get_role(mute_role)
        muted_users = json_reader.get_value(
            f'{interaction.guild.id}/mute_list.json', 'muted_users')
        for item in muted_users:
            if user.id in item:
                try:
                    if role and role in user.roles:
                        muted_users.remove(item)
                        json_reader.set_value(
                            f'{interaction.guild.id}/mute_list.json', 'muted_users', muted_users)
                        await user.remove_roles(role)
                        await interaction.response.send_message(f'{user.mention} был размучен', ephemeral=True)
                    else:
                        await interaction.response.send_message('У выбранного пользователя нет роли `mute`', ephemeral=True)
                except:
                    await interaction.response.send_message(f'Произошла ошибка при размуте {user.mention}.', ephemeral=True)

    @mute.error
    @unmute.error
    async def error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message('У вас нет прав для выполнения этой команды.', ephemeral=True)


def setup(bot):
    bot.add_cog(Mute(bot))
