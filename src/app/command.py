from discord import Color, Game, Status
from discord.ext.commands import Bot, Context

from custom_embed import CustomEmbed, ErrorEmbed
from minecraft import get_online_players, get_server_info, get_server_status


async def on_ready(bot: Bot):
    print(f'{bot.user.name}#{bot.user.discriminator} has connected to Discord!')
    await bot.change_presence(
        activity=Game(name='Minecraft'),
        status=Status.online
    )


class CommandList:
    def __init__(self, minecraft_server: str):
        self.minecraft_server = minecraft_server

    async def address(self, ctx: Context):
        embed = CustomEmbed(
            ctx=ctx,
            title='Server Address',
            description=f'Server address is **{self.minecraft_server}**',
            color=Color.blue()
        )

        await ctx.send(embed=embed)

    async def version(self, ctx: Context):
        response = get_server_info(self.minecraft_server)
        server_status, _ = get_server_status(response)

        if server_status == 'Online':
            embed = CustomEmbed(
                ctx=ctx,
                title='Server Version',
                description=f'Server version is **{response.version.name}**',
                color=Color.gold()
            )
        else:
            embed = ErrorEmbed(
                ctx=ctx,
                title='Server is offline',
                description='Turn on the server to get the version'
            )

        await ctx.send(embed=embed)

    async def status(self, ctx: Context):
        response = get_server_info(self.minecraft_server)
        server_status, color = get_server_status(response)

        embed = CustomEmbed(
            ctx=ctx,
            title='Server Status',
            description=f'Server is **{server_status}**',
            color=color
        )

        await ctx.send(embed=embed)

    async def players(self, ctx: Context):
        response = get_server_info(self.minecraft_server)
        server_status, _ = get_server_status(response)
        success, title, description = get_online_players(
            response, server_status)

        if success:
            embed = CustomEmbed(
                ctx=ctx,
                title=title,
                description=description,
                color=Color.green()
            )
        else:
            embed = ErrorEmbed(
                ctx=ctx,
                title='Server is offline',
                description='Turn on the server to get the players'
            )

        await ctx.send(embed=embed)
