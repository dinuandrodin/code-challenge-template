import sqlite3
import os
import time

# Define database files
DB_WTHR_FILE = "test_weather_data.db"
DATA_DIR = "wx_data"

# Function to Create table if not exists Using SQLite 3 Connection Object
def create_table():
    conn = sqlite3.connect(DB_WTHR_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id TEXT NOT NULL,
            date TEXT CHECK (length(date) = 8) NOT NULL,
            max_temp INTEGER CHECK (max_temp >= -9999),
            min_temp INTEGER CHECK (min_temp >= -9999),
            precipitation INTEGER CHECK (precipitation >= -9999),
            UNIQUE (station_id, date)
        );
    """)
    conn.commit()
    conn.close()

# Function to insert data into the database
def insert_data(file_path):
    conn = sqlite3.connect(DB_WTHR_FILE)
    cursor = conn.cursor()
    
    # Extracting station ID from wx_data/filename
    station_id = os.path.basename(file_path).split('.')[0]  
    inserted_count = 0
    
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split("\t")
            if len(parts) != 4:
                continue  # Skipping invalid lines
            
            date, max_temp, min_temp, precipitation = parts
            
            # Skipping deformed data
            try:
                max_temp, min_temp, precipitation = int(max_temp), int(min_temp), int(precipitation)
            except ValueError:
                continue
            
            # Exception handling to Insert data if not present already
            try:
                cursor.execute("""
                    INSERT INTO test_weather_data (station_id, date, max_temp, min_temp, precipitation)
                    VALUES (?, ?, ?, ?, ?)
                """, (station_id, date, max_temp, min_temp, precipitation))
                inserted_count += 1
            except sqlite3.IntegrityError:
                continue  # Skip duplicates

    conn.commit()
    conn.close()
    return inserted_count  #Writes log output for Number of Records Inserted

# Main function to process all files
def main():
    create_table()  # Ensures that the table exists
    start_time = time.time()
    
    total_inserted = 0
    print("data ingestion Starts...")
    
    for filename in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, filename)
        if os.path.isfile(file_path):
            print(f"Processing {filename}...")
            inserted_count = insert_data(file_path)
            total_inserted += inserted_count
            print(f"{inserted_count} records inserted from {filename}")
    
    end_time = time.time()
    print(f"Data ingestion completed in {end_time - start_time:.2f} seconds.")
    print(f"Total records inserted: {total_inserted}")

if __name__ == "__main__":
    main()
