from discord.ext.commands import Context, check, CheckFailure
from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI'))

db = client['scammer-list']

def lookup_scammer(id: str) -> bool:
    return db['scammers'].find_one({'id': id}) is not None

class NotScammer(CheckFailure):
    pass

def is_scammer():

    async def predicate(ctx: Context) -> bool:

        if not lookup_scammer(ctx.author().id):
            raise NotScammer("You are not a scammer.")
        
        return True

    return check(predicate)