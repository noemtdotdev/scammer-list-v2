from quart import jsonify

route = "/hello"

async def callback():
    return jsonify({"message": "Hello, World!"}), 200
