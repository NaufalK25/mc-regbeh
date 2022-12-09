from discord import Color, Game, Status
from discord.errors import Forbidden
from discord.ext.commands import Bot, Context

import connect
from custom_embed import ChannelCustomEmbed, ContextCustomEmbed, ContextErrorEmbed
from helpers import get_command_list
from minecraft import get_online_players, get_server_data


async def on_ready(bot: Bot):
    print(f'{bot.user.name}#{bot.user.discriminator} has connected to Discord!')
    await bot.change_presence(
        activity=Game(name='Minecraft'),
        status=Status.online
    )


async def server_online_notif_loop(bot: Bot):
    channel_col = connect.database.get_collection('channels')
    channels = channel_col.find({'registered': True})

    for channel_data in channels:
        try:
            channel = bot.get_channel(channel_data['cid'])
            _, server_status, color = get_server_data()

            async for message in channel.history(limit=1):
                if server_status == 'Online':
                    if message.embeds:
                        if 'Online' in message.embeds[0].description:
                            break

                    embed = ChannelCustomEmbed(
                        bot=bot,
                        title='Server Status',
                        description=f'Server is Online',
                        color=color
                    )

                    await channel.send(embed=embed)
                    break
                else:
                    if message.embeds:
                        if 'Offline' in message.embeds[0].description:
                            break

                    embed = ChannelCustomEmbed(
                        bot=bot,
                        title='Server Status',
                        description=f'Server is Offline',
                        color=color
                    )

                await channel.send(embed=embed)
                break
        except Exception:
            continue


class CommandList:
    def __init__(self, minecraft_server: str):
        self.minecraft_server = minecraft_server

    async def help(self, ctx: Context):
        embed = ContextCustomEmbed(
            ctx=ctx,
            title='Help',
            description=f'''Need help?\n- Use `mc command` to get all commands and their descriptions\n- Ask `@NaufalK` for more information''',
            color=Color.gold()
        )

        await ctx.send(embed=embed)

    async def command(self, ctx: Context):
        command_list = get_command_list()

        embed = ContextCustomEmbed(
            ctx=ctx,
            title='Command List',
            description='\n'.join(
                f'**{command}** - {description}' for command, description in command_list.items()
            ),
            color=Color.blue()
        )

        await ctx.send(embed=embed)

    async def register(self, ctx: Context):
        channel_col = connect.database.get_collection('channels')
        channel = channel_col.find_one({'cid': ctx.channel.id})

        if channel and channel['registered']:
            embed = ContextErrorEmbed(
                ctx=ctx,
                title='Channel already registered',
                description='This channel is already registered'
            )

            return await ctx.send(embed=embed)

        if channel and not channel['registered']:
            channel_col.update_one(
                {'cid': ctx.channel.id},
                {'$set': {
                    'registered': True,
                    'register_counter': channel['register_counter'] + 1,
                    'registered_at': ctx.message.created_at
                }}
            )
        else:
            new_channel = {
                'cid': ctx.channel.id,
                'cname': ctx.channel.name,
                'gid': ctx.guild.id,
                'gname': ctx.guild.name,
                'register_counter': 1,
                'unregister_counter': 0,
                'registered': True,
                'registered_at': ctx.message.created_at
            }

            channel_col.insert_one(new_channel)

        embed = ContextCustomEmbed(
            ctx=ctx,
            title='Channel registered',
            description='This channel is now registered',
            color=Color.green()
        )

        await ctx.send(embed=embed)

    async def unregister(self, ctx: Context):
        channel_col = connect.database.get_collection('channels')

        channel = channel_col.find_one({'cid': ctx.channel.id})
        if not channel or not channel['registered']:
            embed = ContextErrorEmbed(
                ctx=ctx,
                title='Channel not registered',
                description='This channel is not registered'
            )

            return await ctx.send(embed=embed)

        channel_col.update_one(
            {'cid': ctx.channel.id},
            {'$set': {
                'registered': False,
                'unregister_counter': channel['unregister_counter'] + 1
            }}
        )

        embed = ContextCustomEmbed(
            ctx=ctx,
            title='Channel unregistered',
            description='This channel is now unregistered',
            color=Color.green()
        )

        await ctx.send(embed=embed)

    async def address(self, ctx: Context):
        embed = ContextCustomEmbed(
            ctx=ctx,
            title='Server Address',
            description=f'Server address is **{self.minecraft_server}**',
            color=Color.blue()
        )

        await ctx.send(embed=embed)

    async def version(self, ctx: Context):
        response, server_status, _ = get_server_data()

        if server_status == 'Online':
            embed = ContextCustomEmbed(
                ctx=ctx,
                title='Server Version',
                description=f'Server version is **{response.version.name}**',
                color=Color.gold()
            )
        else:
            embed = ContextErrorEmbed(
                ctx=ctx,
                title='Server is offline',
                description='Turn on the server to get the version'
            )

        await ctx.send(embed=embed)

    async def status(self, ctx: Context):
        _, server_status, color = get_server_data()

        embed = ContextCustomEmbed(
            ctx=ctx,
            title='Server Status',
            description=f'Server is **{server_status}**',
            color=color
        )

        await ctx.send(embed=embed)

    async def players(self, ctx: Context):
        response, server_status, _ = get_server_data()
        success, title, description = get_online_players(
            response, server_status)

        if success:
            embed = ContextCustomEmbed(
                ctx=ctx,
                title=title,
                description=description,
                color=Color.green()
            )
        else:
            embed = ContextErrorEmbed(
                ctx=ctx,
                title='Server is offline',
                description='Turn on the server to get the players'
            )

        await ctx.send(embed=embed)

    async def clear(sellf, ctx: Context):
        total_chat_count = len(await ctx.channel.history().flatten())

        try:
            while total_chat_count > 0:
                total_chat_count = len(await ctx.channel.history().flatten())

                if total_chat_count == 0:
                    embed = ContextCustomEmbed(
                        ctx=ctx,
                        title='Chat cleared',
                        description='Chat cleared',
                        color=Color.green()
                    )
                    await ctx.send(embed=embed)
        except Forbidden:
            embed = ContextErrorEmbed(
                ctx=ctx,
                title='Missing permission',
                description='Missing Permission, add Manage Messages permmision to this bot if you want to use this command',
            )
            await ctx.send(embed=embed)
        except AttributeError:
            embed = ContextErrorEmbed(
                ctx=ctx,
                title='Can\'t use this command in Direct Message',
                description='Can\'t use this command in Direct Message',
            )
            await ctx.send(embed=embed)
