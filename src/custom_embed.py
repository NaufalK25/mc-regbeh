from discord import Color, Embed
from discord.ext.commands import Context


class CustomEmbed(Embed):
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


class ErrorEmbed(CustomEmbed):
    def __init__(self, ctx: Context, description: str, title: str = 'Error'):
        super().__init__(
            ctx=ctx,
            title=title,
            description=description,
            color=Color.red(),
        )
        self.get_embed_footer(ctx=ctx)
