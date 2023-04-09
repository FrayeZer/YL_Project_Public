from disnake.ext import commands
from disnake import Member, User
import json_reader
import time_events


class Ban(commands.Cog):
    """
    .Cog -> Ban
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description='Забанить участника на сервере.')
    async def ban(self, interaction, user: Member, *, time: str = None, reason: str = None):
        """
        Функция бана участников сервера
        """
        banned_users = json_reader.get_value(f'{interaction.guild.id}/ban_list.json', 'banned_users')
        is_banned = False
        for item in banned_users:
            if user.id in item:
                is_banned = True
        if not is_banned:
            try:
                await user.send(f'Вы были забанены на сервере {interaction.guild.name}. Причина: {reason or "Не указана"}. Срок: {time or "До разбана администратором."}')
                await interaction.guild.ban(user, reason=reason)
                end_time = time_events.get_end_time(time or '3650d')
                banned_users.append([user.id, str(end_time)])
                json_reader.set_value(
                    f'{interaction.guild.id}/ban_list.json', 'banned_users', banned_users)
                await interaction.response.send_message(f'{user.mention} был забанен.', ephemeral=True)
                await interaction.channel.send(f'{user.mention} был забанен администратором {interaction.author.mention}. Причина: {reason or "Не указана"}. Срок: {time or "До разбана администратором"}')
            except:
                await interaction.response.send_message(f'Произошла ошибка при бане {user.mention}.', ephemeral=True)
        else:
            await interaction.response.send_message(f'{user.mention} уже забанен.', ephemeral=True)

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description='Разбанить участника на сервере.')
    async def unban(self, interaction, user: User, *, reason: str = None):
        """
        Функция разбана участников сервера
        """
        banned_users = json_reader.get_value(f'{interaction.guild.id}/ban_list.json', 'banned_users')
        for item in banned_users:
            if user.id in item:
                try:
                    await interaction.guild.unban(user, reason=reason)
                    banned_users.remove(item)
                    json_reader.set_value(
                        f'{interaction.guild.id}/ban_list.json', 'banned_users', banned_users)
                    await interaction.response.send_message(f'{user.mention} был разбанен.', ephemeral=True)
                    await interaction.channel.send(f'{user.mention} был разбанен администратором {interaction.author.mention}. Причина: {reason or "Не указана"}.')
                except:
                    await interaction.response.send_message(f'Произошла ошибка при разбане {user.mention}.', ephemeral=True)
            else:
                if item == banned_users[-1]:
                    await interaction.response.send_message(f'{user.mention} не забанен.', ephemeral=True)

    @ban.error
    @unban.error
    async def ban_error(self, interaction, error):
        """
        Выводит ошибки в случае их возникновения
        """
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message('У вас нет прав для выполнения этой команды.', ephemeral=True)
        elif isinstance(error, commands.BadArgument):
            await interaction.response.send_message('Укажите участника правильно.', ephemeral=True)


def setup(bot):
    bot.add_cog(Ban(bot))
