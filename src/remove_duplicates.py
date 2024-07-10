import logging
from datetime import datetime
from app import app, db
from models import WeatherRecord
from sqlalchemy import func

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def remove_duplicates():
    start_time = datetime.now()
    logger.info(f"Duplicate removal started at {start_time}")
    
    subquery = db.session.query(
        WeatherRecord.date,
        WeatherRecord.max_temp,
        WeatherRecord.min_temp,
        WeatherRecord.precipitation,
        WeatherRecord.weather_station_id,
        func.max(WeatherRecord.ingestion_timestamp).label('max_ingestion_timestamp')
    ).group_by(
        WeatherRecord.date,
        WeatherRecord.max_temp,
        WeatherRecord.min_temp,
        WeatherRecord.precipitation,
        WeatherRecord.weather_station_id
    ).subquery()

    duplicates = db.session.query(WeatherRecord).join(
        subquery,
        (WeatherRecord.date == subquery.c.date) &
        (WeatherRecord.max_temp == subquery.c.max_temp) &
        (WeatherRecord.min_temp == subquery.c.min_temp) &
        (WeatherRecord.precipitation == subquery.c.precipitation) &
        (WeatherRecord.weather_station_id == subquery.c.weather_station_id) &
        (WeatherRecord.ingestion_timestamp != subquery.c.max_ingestion_timestamp)
    ).all()

    duplicate_count = len(duplicates)
    for record in duplicates:
        db.session.delete(record)

    db.session.commit()

    end_time = datetime.now()
    logger.info(f"Duplicate removal finished at {end_time}")
    logger.info(f"Number of duplicate records deleted: {duplicate_count}")
    logger.info(f"Total time taken: {end_time - start_time}")

if __name__ == '__main__':
    with app.app_context():
        remove_duplicates()
