import disnake
import json_reader
from disnake.ext import commands


class Read_File(commands.Cog):
    '''
    .Cog -> ReadFile
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description='Установить роль muted.')
    async def mute_role_set(self, interaction: disnake.ApplicationCommandInteraction, role: disnake.Role):
        json_reader.set_value(f'{interaction.guild.id}/config.json', key='mute_role', data=role.id)
        await interaction.response.send_message(f'Mute роль установлена: {role.mention}', ephemeral=True)

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description='Установить начальную роль.')
    async def join_role_set(self, interaction: disnake.ApplicationCommandInteraction, role: disnake.Role):
        json_reader.set_value(f'{interaction.guild.id}/config.json', key='join_role', data=role.id)
        await interaction.response.send_message(f'Join роль установлена: {role.mention}', ephemeral=True)

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description='Прочитать файл сервера.')
    async def read_file(self, interaction: disnake.ApplicationCommandInteraction, path='config.json', key='all'):
        if key == 'all':
            data = json_reader.open_file(f'{interaction.guild.id}/{path}')
        elif key == 'keys':
            data = list(json_reader.open_file(f'{interaction.guild.id}/{path}').keys())
        else:
            data = json_reader.get_value(f'{interaction.guild.id}/{path}', key)
        await interaction.response.send_message(f'{data}', ephemeral=True)

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description='Изменить файл сервера.')
    async def file_edit(self, interaction: disnake.ApplicationCommandInteraction, key, data, path='config.json'):
        json_reader.set_value(f'{interaction.guild.id}/{path}', key=key, data=data)
        await interaction.response.send_message(f'Значение `{data}` установлено для ключа `{key}`', ephemeral=True)

    @file_edit.error
    @read_file.error
    @mute_role_set.error
    @join_role_set.error
    async def error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message('У вас нет прав для выполнения этой команды.', ephemeral=True)
        else:
            await interaction.response.send_message(f'Произошла ошибка.\n{error}', ephemeral=True)


def setup(bot):
    bot.add_cog(Read_File(bot))
