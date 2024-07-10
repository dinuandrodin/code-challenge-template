from flask import request, jsonify
from flask_restful import Resource
from models import WeatherRecord, WeatherStats
from app import db

# Pagination function
def paginate(query, page, per_page):
    total = query.count()
    items = query.paginate(page, per_page, False).items
    return {
        'total': total,
        'page': page,
        'per_page': per_page,
        'items': [item.to_dict() for item in items]
    }

class WeatherResource(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        date = request.args.get('date', type=str)
        station_id = request.args.get('station_id', type=str)

        query = WeatherRecord.query
        if date:
            query = query.filter(WeatherRecord.date == date)
        if station_id:
            query = query.filter(WeatherRecord.weather_station_id == station_id)

        result = paginate(query, page, per_page)
        return jsonify(result)

class WeatherStatsResource(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        year = request.args.get('year', type=int)
        station_id = request.args.get('station_id', type=str)

        query = WeatherStats.query
        if year:
            query = query.filter(WeatherStats.year == year)
        if station_id:
            query = query.filter(WeatherStats.weather_station_id == station_id)

        result = paginate(query, page, per_page)
        return jsonify(result)
