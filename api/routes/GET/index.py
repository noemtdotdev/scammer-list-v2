from quart import render_template
import os

route = "/"

async def callback():
    return await render_template("index.html")
