from discord import Color, Embed
from discord.ext.commands import Bot, Context


class ContextCustomEmbed(Embed):
    def __init__(self, ctx: Context, title: str, description: str, color: Color):
        super().__init__(
            title=title,
            description=description,
            color=color,
        )
        self.get_embed_footer(ctx=ctx)

    def get_sender_name(self, ctx: Context):
        nickname = ctx.author.display_name
        username = ctx.author.name
        return f"{'(' + nickname + ') ' if nickname != username else ''}{username}#{ctx.author.discriminator}"

    def get_embed_footer(self, ctx: Context):
        self.set_footer(
            text=f"Requested by {self.get_sender_name(ctx=ctx)}",
            icon_url=ctx.author.avatar_url
        )


class ContextErrorEmbed(ContextCustomEmbed):
    def __init__(self, ctx: Context, description: str, title: str = 'Error'):
        super().__init__(
            ctx=ctx,
            title=title,
            description=description,
            color=Color.red(),
        )
        self.get_embed_footer(ctx=ctx)


class ChannelCustomEmbed(Embed):
    def __init__(self, bot: Bot, title: str, description: str, color: Color):
        super().__init__(
            title=title,
            description=description,
            color=color,
        )
        self.get_embed_footer(bot=bot)

    def get_bot_name(self, bot: Bot):
        nickname = bot.user.display_name
        username = bot.user.name
        return f"{'(' + nickname + ') ' if nickname != username else ''}{username}#{bot.user.discriminator}"

    def get_embed_footer(self, bot: Bot):
        self.set_footer(
            text=f"Requested by {self.get_bot_name(bot=bot)}",
            icon_url=bot.user.avatar_url
        )
