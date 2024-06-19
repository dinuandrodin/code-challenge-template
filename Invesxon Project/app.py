from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Welcome10%40@localhost:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
swagger = Swagger(app)

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    max_temp = db.Column(db.Integer)
    min_temp = db.Column(db.Integer)
    precipitation = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint('station_id', 'date', name='_station_date_uc'),)

class YearlyWeatherStats(db.Model):
    __tablename__ = 'yearly_weather_stats'
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_max_temp = db.Column(db.Numeric)
    avg_min_temp = db.Column(db.Numeric)
    total_precipitation = db.Column(db.Numeric)
    __table_args__ = (db.UniqueConstraint('station_id', 'year', name='_station_year_uc'),)

class WeatherDataResource(Resource):
    def get(self):
        station_id = request.args.get('station_id')
        date = request.args.get('date')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        query = WeatherData.query
        if station_id:
            query = query.filter_by(station_id=station_id)
        if date:
            query = query.filter_by(date=date)
        result = query.paginate(page=page, per_page=per_page)

        return jsonify({
            'total': result.total,
            'pages': result.pages,
            'page': result.page,
            'per_page': result.per_page,
            'items': [item.as_dict() for item in result.items]
        })

class WeatherStatsResource(Resource):
    def get(self):
        station_id = request.args.get('station_id')
        year = request.args.get('year')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        query = YearlyWeatherStats.query
        if station_id:
            query = query.filter_by(station_id=station_id)
        if year:
            query = query.filter_by(year=year)
        result = query.paginate(page=page, per_page=per_page)

        return jsonify({
            'total': result.total,
            'pages': result.pages,
            'page': result.page,
            'per_page': result.per_page,
            'items': [item.as_dict() for item in result.items]
        })

def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

WeatherData.as_dict = to_dict
YearlyWeatherStats.as_dict = to_dict

api.add_resource(WeatherDataResource, '/api/weather')
api.add_resource(WeatherStatsResource, '/api/weather/stats')

if __name__ == "__main__":
    app.run(debug=True)
