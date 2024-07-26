from api.api import _api
from bot.bot import _bot
from pymongo import MongoClient

from dotenv import load_dotenv
import os

import asyncio

load_dotenv()

if __name__ == "__main__":

    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client['scammer-list']

    api = _api(db)
    bot = _bot(db)

    loop = asyncio.get_event_loop()
    loop.create_task(api.run_task('0.0.0.0', port=os.getenv('PORT')))
    loop.create_task(bot.start())
    loop.run_forever()
