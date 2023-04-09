import shutil
import os


def on_guild_join(guild):
    default_folder = './app/data/default'
    guild_folder = f'./app/data/{guild.id}'
    if not os.path.exists(guild_folder):
        shutil.copytree(default_folder, guild_folder)


on_guild_join(123)
