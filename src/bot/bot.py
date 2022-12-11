from os import getenv

from discord.ext.commands import Bot, Context
from discord.ext.tasks import loop
from dotenv import load_dotenv

import command
from command import CommandList
from helpers import *

load_dotenv(dotenv_path="./.env")

DEFAULT_PREFIX = 'mc '
bot = Bot(
    case_insensitive=True,
    command_prefix=DEFAULT_PREFIX,
    help_command=None,
    owner_id=getenv('DC_OWNER_ID'),
    self_bot=False
)

command_list = CommandList(minecraft_server=getenv('MC_SERVER'))


@bot.event
async def on_ready():
    @loop(seconds=10)
    async def server_online_notif_loop():
        await command.server_online_notif_loop(bot)

    server_online_notif_loop.start()
    await command.on_ready(bot)


@bot.command(name='help')
async def help_command(ctx: Context):
    await command_list.help(ctx=ctx)


@bot.command(name='command')
async def command_command(ctx: Context):
    await command_list.command(ctx=ctx)


@bot.command(name='register')
async def register_command(ctx: Context):
    await command_list.register(ctx=ctx)


@bot.command(name='unregister')
async def unregister_command(ctx: Context):
    await command_list.unregister(ctx=ctx)


@bot.command(name='address')
async def address_command(ctx: Context):
    await command_list.address(ctx=ctx)


@bot.command(name='version')
async def version_command(ctx: Context):
    await command_list.version(ctx=ctx)


@bot.command(name='status')
async def status_command(ctx: Context):
    await command_list.status(ctx=ctx)


@bot.command(name='players')
async def players_command(ctx: Context):
    await command_list.players(ctx=ctx)


# @bot.command(name='start')
# async def start_command(ctx: Context):
#     await command_list.start(ctx=ctx)


# @bot.command(name='stop')
# async def stop_command(ctx: Context):
#     await command_list.stop(ctx=ctx)


# @bot.command(name='restart')
# async def restart_command(ctx: Context):
#     await command_list.restart(ctx=ctx)


if is_app_mode('development'):
    @bot.command(name='clear')
    async def clear_command(ctx: Context):
        await command_list.clear(ctx=ctx)


if __name__ == '__main__':
    bot.run(getenv('DC_TOKEN'))
