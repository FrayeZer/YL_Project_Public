import disnake
import os
from disnake.ext import commands
import asyncio
import concurrent.futures
import time_events
import json_reader
import shutil

token = 'MTA4' + 'OTg2NzAyMzgyN' + 'TI2MDYwNQ.GZUIWM.' + 'yrtB4tBQGHQk8' + 'U709HkeMZr' + '71ZsxJ8' + 'l3Y9-vxg'
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix='yl!', intents=intents,
                   help_command=None)
# test_guilds=[1091696941341094018, 1094370946221088948]

try:
    for file in os.listdir('./app/bot/cogs'):
        if file.endswith('.py'):
            bot.load_extension(f'cogs.{file[:-3]}')
except Exception:
    for file in os.listdir('./bot/cogs'):
        if file.endswith('.py'):
            bot.load_extension(f'cogs.{file[:-3]}')


async def event_loop():
    '''
    Цикл событий для работы с функциями, зависящими от времени
    '''
    while True:
        await time_events.execute_actions(bot=bot)
        await asyncio.sleep(30)


@bot.event
async def on_ready():
    '''
    Выполняется при запуске бота
    '''
    print('bot_status: online')
    activity = disnake.Activity(name='Решает задачи в YL',
                        type=disnake.ActivityType.playing)
    await bot.change_presence(activity=activity)

    for guild in bot.guilds:
        for member in guild.members:
            if member.guild_permissions.administrator and not member.bot:
                await member.send('Бот теперь онлайн')

    # Запуск функции event_loop в отдельном потоке с помощью метода run_in_executor.
    # Спасибо chatgpt за подсказку.
    with concurrent.futures.ThreadPoolExecutor() as pool:
        await bot.loop.run_in_executor(pool, await event_loop())


@bot.event
async def on_member_join(member):
    '''
    Автоматическая выдача начальной роли зашедшему на сервер участнику
    '''
    guild = member.guild
    join_role_id = json_reader.get_value(
        f'{guild.id}/config.json', 'join_role')
    if join_role_id:
        role = guild.get_role(join_role_id)
        await member.add_roles(role)


@bot.event
async def on_guild_join(guild):
    '''
    Отвечает за создание папки с файлами бота для конкретного сервера
    '''
    try:
        default_folder = './app/data/default'
        guild_folder = f'./app/data/{guild.id}'
        if not os.path.exists(guild_folder):
            shutil.copytree(default_folder, guild_folder)
    except Exception:
        default_folder = './data/default'
        guild_folder = f'./data/{guild.id}'
        if not os.path.exists(guild_folder):
            shutil.copytree(default_folder, guild_folder)


if __name__ == '__main__':
    bot.run(token)
