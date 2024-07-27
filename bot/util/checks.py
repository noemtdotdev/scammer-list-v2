from discord.ext.commands import Context, check, CheckFailure
from pymongo import MongoClient

import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv('MONGODB_URI'))

db = client['scammer-list']

class NotScammer(CheckFailure):
    pass

class NotStaff(CheckFailure):
    pass

def is_scammer():

    async def predicate(ctx: Context) -> bool:

        if db['scammers'].find_one({'id': str(ctx.author.id)}) is None:
            raise NotScammer("You are not a scammer.")
        
        return True

    return check(predicate)

def is_staff():
    async def predicate(ctx: Context) -> bool:
        if db['staff'].find_one({'id': int(ctx.author.id)}) is None:
            raise NotStaff("You are not a staff member.")
        
        return True
    
    return check(predicate)
