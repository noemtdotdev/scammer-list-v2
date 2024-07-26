from quart import jsonify, current_app
from api.auth import verify_api_key

route = "/api/get-scammers"

@verify_api_key
async def callback():
    collection = current_app.db["scammers"]

    cursor = collection.find({}, {"_id": 0})
    scammers = [document for document in cursor]
    
    return jsonify({"success": True, "data": scammers}), 200
