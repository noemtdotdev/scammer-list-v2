import discord
from discord.ext import commands
from discord import SlashCommandGroup, option
from bot.bot import Bot
from bot.util.embed import embed_generator

class ManageStaff(commands.Cog):
    def __init__(self, bot):
        self.bot:Bot = bot

    staff = SlashCommandGroup("staff", "Staff management commands", integration_types={discord.IntegrationType.user_install, discord.IntegrationType.guild_install})

    @staff.command(
        name="add",
        description="Adds a staff member to the list."
    )
    @option(
        name="user",
        description="The user to add to the staff list.",
        type=discord.User,
        required=True
    )
    @commands.is_owner()
    async def _staff_add(self, ctx: discord.ApplicationContext, user: discord.User):
        staff_collection = self.bot.db["staff"]
        staff = staff_collection.find_one({'id': user.id})

        if staff:
            return await ctx.respond(embed=embed_generator(title="Error", description="This person is already a staff member."))
        
        staff_collection.insert_one({
            'owner': False,
            'id': user.id,
            'username': user.name,
            'nick': user.global_name,
        })

        self.bot.staff.append(user.id)

        await ctx.respond(embed=embed_generator(title="Success", description=f"{user.mention} has been added to the staff list.", color=discord.Color.green()))

    
    @staff.command(
        name="remove",
        description="Removes a staff member from the list."
    )
    @option(
        name="user",
        description="The user to remove from the staff list.",
        type=discord.User,
        required=True
    )
    @commands.is_owner()
    async def _staff_remove(self, ctx: discord.ApplicationContext, user: discord.User):
        staff_collection = self.bot.db["staff"]
        staff = staff_collection.find_one_and_delete({'id': user.id})

        if not staff:
            return await ctx.respond(embed=embed_generator(title="Error", description="This person is not a staff member."))
        
        staff_collection.delete_one({'id': user.id})

        self.bot.staff.remove(user.id)
        
        await ctx.respond(embed=embed_generator(title="Success", description=f"{user.mention} has been removed from the staff list.", color=discord.Color.green()))

def setup(bot:Bot):
    bot.add_cog(ManageStaff(bot))