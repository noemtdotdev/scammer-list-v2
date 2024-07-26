from quart import jsonify
from api.auth import verify_api_key

route = "/hello"

@verify_api_key
async def callback():
    return jsonify({"message": "Hello, World!"}), 200
