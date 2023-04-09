from datetime import datetime, timedelta
from json_reader import open_file
import json_reader
import disnake
import os
import shutil

duration = {
    'm': 'minutes',
    'h': 'hours',
    'd': 'days',
    'w': 'weeks'
}


def get_end_time(time) -> str:
    '''
    Функция рассчета времени события
    '''
    num = int(time[:-1])
    time = time[-1]
    if time not in duration:
        raise ValueError(
            'Неправильный формат времени')
    now = datetime.now()
    dur = {duration[time]: num}
    end_time = now + timedelta(**dur)
    return end_time.strftime('%d-%m-%Y %H:%M:%S')


def time_is_up(time) -> bool:
    '''
    Функция сравнения текущей даты и времени и введенной. Возвращает True, текущая дата позже введенной, иначе - False
    '''
    now = datetime.now()
    timetime = datetime.strptime(time, '%d-%m-%Y %H:%M:%S')
    if now > timetime:
        return True
    return False


def get_unban_actions(guild_id):
    actions = open_file(path=f'{guild_id}/ban_list.json')['banned_users']
    return actions


def get_unmute_actions(guild_id):
    actions = open_file(path=f'{guild_id}/mute_list.json')['muted_users']
    return actions


async def execute_actions(bot):
    for guild in bot.guilds:
        try:
            banned_users = get_unban_actions(guild.id)
            for act in banned_users:
                if time_is_up(act[1]):
                    member = disnake.Object(id=act[0])
                    await guild.unban(member, reason='Время бана истекло.')
                    banned_users.remove(act)
                    json_reader.set_value(
                        f'{guild.id}/ban_list.json', 'banned_users', banned_users)
        except Exception as e:
            print(e)
            
        try:
            muted_users = get_unmute_actions(guild.id)
            for act in muted_users:
                if time_is_up(act[1]):
                    member = guild.get_member(act[0])
                    mute_role = json_reader.get_value(
                        f'{guild.id}/config.json', 'mute_role')
                    role = guild.get_role(mute_role)
                    await member.remove_roles(role)
                    muted_users.remove(act)
                    json_reader.set_value(
                        f'{guild.id}/mute_list.json', 'muted_users', muted_users)
        except Exception as e:
            print(e)
