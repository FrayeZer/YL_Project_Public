from disnake.ext import commands
from chatgpt_responser import chatgpt_response


class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(description='Чат с chatgpt.')
    async def gpt(self, interaction, prompt: str):
        await interaction.response.defer()

        msg = chatgpt_response(interaction, prompt)

        await interaction.followup.send(msg)


def setup(bot):
    bot.add_cog(Gpt(bot))
