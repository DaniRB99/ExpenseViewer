from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from .models import transacs

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    app.config["MONGO_URI"] = "mongodb://localhost:27017/"
    Api(app)
    app.register_blueprint(transacs)
    app.url_map.strict_slashes = False
    
    CORS(app, resources={
        r"/api/v1/*": {
            "origins": "http://localhost:5173"
        }
    })
    
    # app.run(host="localhost", port=8000, debug=True)
    return app

# def start_app(config_filename=None):
if __name__ == "__main__":
    app = Flask(__name__)
    # app.config.from_pyfile(config_filename)
    Api(app)
    app.register_blueprint(transacs)
    app.url_map.strict_slashes = False
    app.run(host="localhost", port=8000, debug=True)
