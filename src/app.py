from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    api = Api(app)

    from resources import WeatherResource, WeatherStatsResource
    api.add_resource(WeatherResource, '/api/weather')
    api.add_resource(WeatherStatsResource, '/api/weather/stats')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
