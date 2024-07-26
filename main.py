from api.api import api
from bot.bot import bot

from dotenv import load_dotenv
import os

import asyncio

load_dotenv()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.create_task(api().run_task('0.0.0.0', port=os.getenv('PORT')))
    loop.create_task(bot().start())
    loop.run_forever()
