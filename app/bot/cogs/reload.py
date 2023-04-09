from disnake.ext import commands
import traceback


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.slash_command()
    async def reload(self, interaction, cog_name: str = 'all'):
        if cog_name.lower() == 'all':
            try:
                cogs = list(self.bot.cogs.keys())
                for cog in cogs:
                    self.bot.reload_extension(f'cogs.{cog.lower()}')
                await interaction.response.send_message('Все модули были перезагружены', ephemeral=True)
            except Exception as e:
                error_msg = f'Ошибка при перезагрузке модулей: {e}\n\n{traceback.format_exc()}'
                await interaction.response.send_message(error_msg, ephemeral=True)
        else:
            try:
                self.bot.reload_extension(f'cogs.{cog_name.lower()}')
                await interaction.response.send_message(f'Перезагружен модуль `{cog_name.lower()}`', ephemeral=True)
            except Exception as e:
                error_msg = f'Ошибка при перезагрузке модуля `{cog_name.lower()}`: {e}\n\n{traceback.format_exc()}'
                await interaction.response.send_message(error_msg, ephemeral=True)

    @reload.error
    async def reload_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message('У вас нет прав для выполнения этой команды.', ephemeral=True)


def setup(bot):
    bot.add_cog(Reload(bot))
