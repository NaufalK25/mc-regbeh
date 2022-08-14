from os import getenv

from discord.ext.commands import Bot, Context
from dotenv import load_dotenv

import command
from command import CommandList
from keep_alive import keep_alive

load_dotenv(dotenv_path="./.env")

DEFAULT_PREFIX = 'mc '
bot = Bot(
    case_insensitive=True,
    command_prefix=DEFAULT_PREFIX,
    help_command=None,
    owner_id=getenv('DC_OWNER_ID'),
    self_bot=False
)

if __name__ == '__main__':
    command_list = CommandList(minecraft_server=getenv('MC_SERVER'))

    @bot.event
    async def on_ready():
        await command.on_ready(bot)

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

    keep_alive()
    bot.run(getenv('DC_TOKEN'))
