import sys
import os
from disnake.ext import commands


class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.slash_command()
    async def restart(self, interaction):
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.guild_permissions.administrator and not member.bot:
                    try:
                        await member.send('Бот будет перезагружен')
                    except Exception:
                        pass
        await interaction.response.send_message('Перезагрузка...', ephemeral=True)
        os.execl(sys.executable, sys.executable, *sys.argv)

    @restart.error
    async def reload_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message('У вас нет прав для выполнения этой команды.', ephemeral=True)


def setup(bot):
    bot.add_cog(Restart(bot))
