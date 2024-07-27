from quart import send_file
import os

route = "/assets/<query>"

async def callback(query:str):
    if os.path.exists(f"files/{query}"):
        return await send_file(f"files/{query}")
    
    return {"success": False, "error": "File not found"}, 404
