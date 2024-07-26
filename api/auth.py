from quart import request, jsonify, current_app
from functools import wraps

def verify_api_key(func):

    @wraps(func)
    async def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Authorization') or request.args.get('key')

        if api_key != current_app.config['API_KEY']:
            return jsonify({"success": False, "error": "Invalid API key"}), 401
        
        return await func(*args, **kwargs)
    
    return decorated_function
