import os
import glob
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import pandas as pd


# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = "postgresql://postgres:Welcome10%40@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    station_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    max_temp = Column(Integer)
    min_temp = Column(Integer)
    precipitation = Column(Integer)
    __table_args__ = (UniqueConstraint('station_id', 'date', name='_station_date_uc'),)

Base.metadata.create_all(engine)

def ingest_data(file_path):
    try:
        logger.info(f"Starting data ingestion from {file_path}")
        start_time = datetime.now()
        record_count = 0
        with open(file_path, 'r') as file:
            for line in file:
                date_str, max_temp, min_temp, precipitation = line.strip().split('\t')
                if int(max_temp) == -9999: max_temp = None
                if int(min_temp) == -9999: min_temp = None
                if int(precipitation) == -9999: precipitation = None
            
                weather_record = WeatherData(
                    station_id=os.path.basename(file_path).split('.')[0],
                    date=datetime.strptime(date_str, '%Y%m%d').date(),
                    max_temp=max_temp,
                    min_temp=min_temp,
                    precipitation=precipitation
                )
                session.merge(weather_record)
                record_count += 1

        session.commit()
        end_time = datetime.now()
        logger.info(f"Completed data ingestion from {file_path} with {record_count} records in {end_time - start_time}")
    except:
        print("This data is already exists")

if __name__ == "__main__":
    data_files = glob.glob("wx_data/*.txt")
    for file_path in data_files:
        ingest_data(file_path)



try:
    conn = psycopg2.connect("dbname=postgres user=postgres password=Welcome10@ host=localhost port=5432")
    print("Connection successful")
except Exception as e:
    print(f"Error connecting to the database: {e}")

con=conn.cursor()
# df=pd.read_sql("with new_table as (select *,date_part('year',date) as Year from weather_data) select station_id,year,avg(max_temp) as avg_maxtemp,avg(min_temp) as avg_mintemp,sum(precipitation) as total_precipitation  from new_table group by station_id,year",conn)
con.execute("create table if not exists postgres.public.mytab as select station_id,date_part('year',date) as year,avg(max_temp) as avg_maxtemp,avg(min_temp) as avg_mintemp,sum(precipitation) as total_precipitation  from weather_data group by station_id,year")
conn.commit()
