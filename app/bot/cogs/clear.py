from disnake.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.slash_command(description='Очистить чат.')
    async def clear(self, interaction, amount: int):
        await interaction.response.defer()
        channel = interaction.channel
        await channel.purge(limit=amount + 1)

    @clear.error
    async def reload_error(self, interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message('У вас нет прав для выполнения этой команды.', ephemeral=True)


def setup(bot):
    bot.add_cog(Clear(bot))
