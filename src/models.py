from datetime import datetime
from app import db

class WeatherRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(8), nullable=False, index=True)
    max_temp = db.Column(db.Integer, nullable=True)
    min_temp = db.Column(db.Integer, nullable=True)
    precipitation = db.Column(db.Integer, nullable=True)
    weather_station_id = db.Column(db.String, nullable=False, index=True)
    ingestion_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        db.Index('idx_date_station', 'date', 'weather_station_id'),
    )

    def __repr__(self):
        return f'<WeatherRecord {self.date} {self.weather_station_id}>'

class WeatherStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    weather_station_id = db.Column(db.String, nullable=False, index=True)
    avg_max_temp = db.Column(db.Float, nullable=True)
    avg_min_temp = db.Column(db.Float, nullable=True)
    total_precipitation = db.Column(db.Float, nullable=True)

    __table_args__ = (
        db.Index('idx_year_station', 'year', 'weather_station_id'),
    )

    def __repr__(self):
        return f'<WeatherStats {self.year} {self.weather_station_id}>'
