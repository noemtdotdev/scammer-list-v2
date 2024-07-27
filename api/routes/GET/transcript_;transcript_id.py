from quart import jsonify, render_template
import os

route = "/transcript/<transcript_id>"

async def callback(transcript_id:str):

    if os.path.exists(f"api/templates/{transcript_id}.html"):
        return await render_template(f"api/templates/{transcript_id}")

    return jsonify({"success": False, "error": f"Transcript '{transcript_id}' not Found"}), 404
