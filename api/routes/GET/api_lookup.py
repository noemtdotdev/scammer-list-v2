from quart import jsonify, current_app
from api.functions.is_match import is_match

route = "/api/lookup/<query>"

async def callback(query:str):
    collection = current_app.db["scammers"]

    data = []
    scammers_data = collection.find({}, {'_id': 0})

    for scammer in scammers_data:
        if is_match(scammer, query):
            data.append(scammer)

    return jsonify({"success": True, "data": data}), 200
