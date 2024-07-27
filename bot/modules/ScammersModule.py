import discord
from discord.ext import commands
from discord import SlashCommandGroup, option
from bot.bot import Bot
from bot.util.embed import embed_generator
from bot.views.scammerlookup import ScammerLookupView 
from bot.util.checks import is_staff

class ScammersModule(commands.Cog):
    def __init__(self, bot):
        self.bot:Bot = bot

    def is_match(self, scammer, arguments):
        for key, value in scammer.items():
            if isinstance(value, str) and arguments.lower() in value.lower():
                return True
            elif isinstance(value, list):
                if any(isinstance(item, str) and arguments.lower() in item.lower() for item in value):
                    return True
        return False

    scammers = SlashCommandGroup("scammers", "Scammer related commands.", integration_types={discord.IntegrationType.user_install, discord.IntegrationType.guild_install})

    @scammers.command(
        name="lookup",
        description="Look up a scammer by his info.",
    )
    @option(
        name="query",
        description="Text to scan the database for.",
        type=str,
        required=True,
    )
    async def lookup(self, ctx: discord.ApplicationContext, query: str):
        collection = self.bot.db["scammers"]

        data = []
        scammers_data = collection.find({})

        for scammer in scammers_data:
            if self.is_match(scammer, query):
                data.append(scammer)

        if not data:
            return await ctx.respond(embed=embed_generator(title="Scammer Lookup", description=f"No scammers found for given query: `{query}`."))

        view = ScammerLookupView(scammer_data=data)
        embed = view.generate_embed()

        await ctx.respond(embed=embed, view=view)

    @scammers.command(
        name="get-all",
        description="Get all scammers in the database.",
    )
    async def lookup(self, ctx: discord.ApplicationContext):
        collection = self.bot.db["scammers"]

        data = []
        scammers_data = collection.find({})

        for scammer in scammers_data:
            data.append(scammer)

        if not data:
            return await ctx.respond(embed=embed_generator(title="Scammer Lookup", description=f"No scammers found in the database."))

        view = ScammerLookupView(scammer_data=data)
        embed = view.generate_embed()

        await ctx.respond(embed=embed, view=view)

    
    @scammers.command(
        name="add",
        description="Add a new scammer to the database.",
    )
    @is_staff()
    @option(
        name="user",
        description="The user to add to the database.",
        type=str,
        required=True,
    )
    @option(
        name="method",
        description="The method of scamming.",
        type=str,
        required=True,
        choices=[
            "OAuth Ratting.",
            "Regular Ratting.",
            "Coin Scamming.",
            "Account Scamming.",
            "Middleman Scamming.",
            "Impersonating to Scam.",
            "Selling stolen Accounts purposefully without offering warranty.",
            "Alt Account of Scammer.",
            "Profile Scamming",
            "Account Phishing",
            "Other"
        ]
    )
    @option(
        name="amount",
        description="The amount of money or items that was scammed.",
        type=str,
        required=True,
    )
    async def add(self, ctx: discord.ApplicationContext, user: str, method: str, amount: str):

        if not user.isdigit():
            return await ctx.respond(embed=embed_generator(title="Invalid User ID", description="Please provide a valid user"))

        try:
            user_object = await self.bot.fetch_user(user)
        except discord.errors.NotFound:
            return await ctx.respond(embed=embed_generator(title="User Not Found", description="Perhaps he got terminated?"))
        

        scammers_collection = self.bot.db["scammers"]

        if scammers_collection.find_one({'id': user_object.id}):
            return await ctx.respond(embed=embed_generator(title="Error", description="This person is already in the database."))
        
        channel = self.bot.get_channel(1266694726195609630)
        message = await channel.send(
            embed=embed_generator(
                title="New Scammer Added",
                description=(
                    f"User: `{user_object.name}` {user_object.mention}\n"
                    f"ID: `{user_object.id}`\n"
                    f"Method: `{method}`\n"
                    f"Amount Scammed: `{amount}`\n\n"
                    f"Added by: {ctx.author.mention}"
                )).set_thumbnail(url=user_object.avatar.url if user_object.avatar else user_object.default_avatar.url)
            )

        scammers_collection.insert_one({
            'listed_by': str(ctx.author.id),
            'message_id': str(message.id),
            'id': str(user_object.id),
            'username': user_object.name,
            'method': method,
            'amount': amount,
            'previous_aliases': []
        })

        await ctx.respond(embed=embed_generator(title="Scammer Added", description=f"Scammer `{user_object.name}` added to the database. Method: {method}, Amount: {amount}", color=discord.Color.green()))

    
    @scammers.command(
        name="remove",
        description="Remove a scammer from the database.",
    )
    @is_staff()
    @option(
        name="user",
        description="The user to remove from the database.",
        type=str,
        required=True
    )
    async def remove(self, ctx: discord.ApplicationContext, user: str):
        scammers_collection = self.bot.db["scammers"]

        if not user.isdigit():
            return await ctx.respond(embed=embed_generator(title="Invalid User ID", description="Please provide a valid user"))    
        
        if int(user) == ctx.author.id:
            return await ctx.respond(embed=embed_generator(title="Error", description="You cannot remove yourself."))

        scammer = scammers_collection.find_one({'id': user})
        if not scammer:
            return await ctx.respond(embed=embed_generator(title="Error", description="This person is not in the database."))
        
        scammers_collection.delete_one({'id': user})
        
        if scammer.get('message_id'):
            channel = self.bot.get_channel(1266694726195609630)
            message = await channel.fetch_message(int(scammer['message_id']))
            if message:
                await message.delete()

        
        await ctx.respond(embed=embed_generator(title="Scammer Removed", description=f"Scammer `{scammer['username']}` removed from the database.", color=discord.Color.red()))


    @scammers.command(
        name="update",
        description="Update a scammer's information in the database.",
    )
    @is_staff()
    @option(
        name="user",
        description="The user to update.",
        type=str,
        required=True
    )
    @option(
        name="method",
        description="The method of scamming.",
        type=str,
        required=False,
        choices=[
            "OAuth Ratting.",
            "Regular Ratting.",
            "Coin Scamming.",
            "Account Scamming.",
            "Middleman Scamming.",
            "Impersonating to Scam.",
            "Selling stolen Accounts purposefully without offering warranty.",
            "Alt Account of Scammer.",
            "Profile Scamming",
            "Account Phishing",
            "Other"
        ])
    @option(
        name="amount",
        description="The amount of money or items that was scammed.",
        type=str,
        required=False,
    )
    async def update(self, ctx: discord.ApplicationContext, user: str, method: str = None, amount: str = None):

        if not method and not amount:
            return await ctx.respond(embed=embed_generator(title="Error", description="Please provide a method or an amount to update."))
        
        if not user.isdigit():
            return await ctx.respond(embed=embed_generator(title="Invalid User ID", description="Please provide a valid user"))
                
        if int(user) == ctx.author.id:
            return await ctx.respond(embed=embed_generator(title="Error", description="You cannot update yourself."))
        
        scammers_collection = self.bot.db["scammers"]
        scammer = scammers_collection.find_one({'id': user})
        if not scammer:
            return await ctx.respond(embed=embed_generator(title="Error", description="This person is not in the database."))
        
        if method:
            scammer['method'] = method
            scammers_collection.update_one({'id': user}, {'$set': {'method': method}})

        if amount:
            scammer['amount'] = amount
            scammers_collection.update_one({'id': user}, {'$set': {'amount': amount}})

        await ctx.respond(embed=embed_generator(title="Scammer Updated", description=f"Scammer `{scammer['username']}` updated.", color=discord.Color.green()))

        if scammer.get('message_id'):
            channel = self.bot.get_channel(1266694726195609630)
            message = await channel.fetch_message(int(scammer['message_id']))
            if message:
                await message.edit(embed=embed_generator(
                title="New Scammer Added",
                description=(
                    f"User: `{scammer['username']}` <@{scammer['id']}>\n"
                    f"ID: `{scammer['id']}`\n"
                    f"Method: `{scammer['method']}`\n"
                    f"Amount Scammed: `{scammer['amount']}`\n\n"
                    f"Added by: <@{scammer['listed_by']}>\n"
                    f"Updated by: {ctx.author.mention}"
                )).set_thumbnail(url=message.embeds[0].thumbnail.url)
            )

def setup(bot:Bot):
    bot.add_cog(ScammersModule(bot))