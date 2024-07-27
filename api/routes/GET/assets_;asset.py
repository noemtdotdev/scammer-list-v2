from quart import send_file
import os

route = "/assets/<asset>"

async def callback(query:str):
    if os.path.exists(f"api/files/{query}"):
        return await send_file(f"api/files/{query}")
    
    return {"success": False, "error": "File not found"}, 404
