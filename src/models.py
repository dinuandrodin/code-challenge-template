from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'max_temp': self.max_temp,
            'min_temp': self.min_temp,
            'precipitation': self.precipitation,
            'weather_station_id': self.weather_station_id,
            'ingestion_timestamp': self.ingestion_timestamp.isoformat()
        }

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

    def to_dict(self):
        return {
            'id': self.id,
            'year': self.year,
            'weather_station_id': self.weather_station_id,
            'avg_max_temp': self.avg_max_temp,
            'avg_min_temp': self.avg_min_temp,
            'total_precipitation': self.total_precipitation
        }

    def __repr__(self):
        return f'<WeatherStats {self.year} {self.weather_station_id}>'
