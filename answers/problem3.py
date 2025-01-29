import sqlite3
import time

DB_FILE = "test_weather_data.db"

# Function to Create the weather_summary table if it does not exist
def create_summary_table():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id TEXT NOT NULL,
            year TEXT NOT NULL,
            avg_max_temp REAL,  -- Stored in degrees Celsius
            avg_min_temp REAL,  -- Stored in degrees Celsius
            total_precipitation REAL, -- Stored in centimeters
            UNIQUE (station_id, year)
        );
    """)
    conn.commit()
    conn.close()

# Function to Compute yearly statistics and stores them in weather_summary
def compute_and_store_summary():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    start_time = time.time()
    print("Computing yearly weather statistics...")

    # Query to compute yearly statistics (Averages of Max, Min Temp AND Sum of Precipitation )
    cursor.execute("""
        INSERT OR REPLACE INTO weather_summary (station_id, year, avg_max_temp, avg_min_temp, total_precipitation)
        SELECT 
            station_id,
            SUBSTR(date, 1, 4) AS year,
            AVG(NULLIF(max_temp, -9999)) / 10.0 AS avg_max_temp, 
            AVG(NULLIF(min_temp, -9999)) / 10.0 AS avg_min_temp, 
            SUM(NULLIF(precipitation, -9999)) / 100.0 AS total_precipitation
        FROM test_weather_data
        GROUP BY station_id, year;
    """)

    conn.commit()
    conn.close()
    
    end_time = time.time()
    print(f"Yearly statistics computed and stored in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    create_summary_table()
    compute_and_store_summary()
