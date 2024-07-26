import discord
from discord.ext import commands
import traceback

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.ApplicationCommandError):
        try:
            if isinstance(error, commands.CommandOnCooldown):
                embed = discord.Embed(color=discord.Color.brand_red(), title="An Error Occured.", description=f"You are on cooldown for this command. Try again in \
                                                    {error.retry_after:.2f} seconds.")
                embed.set_footer(
                    text="Made by notnomv6", icon_url="https://bots.noemt.dev/avatars/nom.png")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.MissingPermissions):
                MissingPermissions = ""
                for perm in error.missing_permissions:
                    MissingPermissions += f"`{perm}` "
                embed = discord.Embed(color=discord.Color.brand_red(
                ), title="An Error Occured.", description=f"You need the {MissingPermissions} permissions to execute this command.")
                embed.set_footer(
                    text="Made by notnomv6", icon_url="https://bots.noemt.dev/avatars/nom.png")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.MissingRole):
                MissingRole = ""
                for role in error.missing_role:
                    MissingRole += f"`{role}` "
                embed = discord.Embed(color=discord.Color.brand_red(
                ), title="An Error Occured.", description=f"You need the {MissingRole} role to execute this command.")
                embed.set_footer(
                    text="Made by notnomv6", icon_url="https://bots.noemt.dev/avatars/nom.png")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.NotOwner):
                embed = discord.Embed(color=discord.Color.brand_red(
                ), title="An Error Occured.", description=f"You need to be a bot owner to execute this command.")
                embed.set_footer(
                    text="Made by notnomv6", icon_url="https://bots.noemt.dev/avatars/nom.png")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.BotMissingPermissions):
                BotMissingPermissions = ""
                for i in error.missing_permissions:
                    BotMissingPermissions += f"`{i}`"

                embed = discord.Embed(color=discord.Color.brand_red(
                ), title="An Error Occured.", description=f"I need the {BotMissingPermissions} permissions to execute this command.")
                embed.set_footer(
                    text="Made by notnomv6", icon_url="https://bots.noemt.dev/avatars/nom.png")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.NoPrivateMessage):
                embed = discord.Embed(color=discord.Color.brand_red(
                ), title="An Error Occured.", description=f"This command cannot be used in private messages.")
                embed.set_footer(
                    text="Made by notnomv6", icon_url="https://bots.noemt.dev/avatars/nom.png")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.PrivateMessageOnly):
                embed = discord.Embed(color=discord.Color.brand_red(
                ), title="An Error Occured.", description=f"This command can only be used in private messages.")
                embed.set_footer(
                    text="Made by notnomv6", icon_url="https://bots.noemt.dev/avatars/nom.png")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, commands.errors.CheckAnyFailure):
                embed = discord.Embed(color=discord.Color.brand_red(
                ), title="An Error Occured.", description=f"You do not have the required role(s) to use this command.")
                embed.set_footer(
                    text="Made by notnomv6", icon_url="https://bots.noemt.dev/avatars/nom.png")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            elif isinstance(error, discord.errors.NotFound):
                embed = discord.Embed(color=discord.Color.brand_red(
                ), title="An Error Occured.", description=f"Interaction failed to respond in time. Try again later.")
                embed.set_footer(
                    text="Made by notnomv6", icon_url="https://bots.noemt.dev/avatars/nom.png")
                await ctx.respond(embed=embed, ephemeral=True)
                return

            else:
                error = getattr(error, 'original', error)
                error = traceback.format_exception(
                    type(error), error, error.__traceback__)
                error = ''.join(error)

                embed = discord.Embed(color=discord.Color.brand_red(
                ), title="An Error Occured.", description=f"An error occured: ```{error}```, please report this to `notnomv6` along with how this issue occured.")
                embed.set_footer(
                    text="Made by notnomv6", icon_url="https://bots.noemt.dev/avatars/nom.png")
                await ctx.respond(embed=embed, ephemeral=True)
                return

        except discord.HTTPException:
            traceback.print_exc()


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
