from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flasgger import Swagger
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object('config')

    db.init_app(app)

    api = Api(app)

    from resources import WeatherResource, WeatherStatsResource
    api.add_resource(WeatherResource, '/api/weather')
    api.add_resource(WeatherStatsResource, '/api/weather/stats')

    # Add Swagger documentation
    swagger = Swagger(app)

    return app

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
