from quart import Quart
from quart_cors import cors
import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

class App(Quart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.api_key = os.getenv('API_KEY')
        self.api_url = os.getenv('API_URL')
        self.db = MongoClient(os.getenv('MONGODB_URI'))['scammer-list']

        self.config['API_KEY'] = self.api_key

methods = ['GET', 'POST']

def _api() -> App:

    app = App(__name__)
    app = cors(app)

    for method in methods:
        for file in os.listdir(f'api/routes/{method}'):
            if file.endswith('.py'):

                route = __import__(f"api.routes.{method}.{file[:-3]}", fromlist=["route", "callback"])
                endpoint = f"{method}_{file[:-3]}"

                app.add_url_rule(route.route, endpoint, route.callback, methods=[method])
                print(f"Added route {route.route} with method {method}.")


    return app
