# Weather Data API

## Purpose

This project provides a RESTful API to manage and query weather data records. It allows users to retrieve weather records and statistics for different weather stations, ensuring robust data validation, error handling, and pagination.

## Project Structure

- **models.py**: Contains SQLAlchemy models representing the weather records and statistics.
- **load_data.py**: Script to load weather data from `.txt` files into the SQLite database.
- **calculate_statistics.py**: Script to calculate yearly weather statistics for each weather station and store them in the database.
- **remove_duplicates.py**: Script to remove duplicate records from the database, keeping only the latest record based on the ingestion timestamp.
- **test_app.py**: Contains unit tests to ensure the API endpoints function correctly and meet specified requirements.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Requirements**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run Data Ingestion**

   ```bash
   python load_data.py
   ```

6. **Perform Data Analytics Task**

   ```bash
   python calculate_statistics.py
   ```

7. **Launch the API**

   ```bash
   python app.py
   ```

8. **Access the Swagger UI**

   Open your web browser and navigate to `http://127.0.0.1:5000/apidocs` to access the Swagger UI for the API documentation.

## API Endpoints

### `/api/weather`
- **Description**: Retrieve weather records.
- **Method**: `GET`
- **Parameters**:
  - `page` (optional): Page number for pagination (integer).
  - `per_page` (optional): Number of records per page (integer).
  - `date` (optional): Filter by date in `YYYY-MM-DD` format (string).
  - `station_id` (optional): Filter by station ID (string).
- **Responses**:
  - `200 OK`: Successfully retrieved weather records.
    ```json
    {
      "total": 2,
      "page": 1,
      "per_page": 10,
      "items": [
        {
          "id": 1,
          "date": "20230101",
          "max_temp": 250,
          "min_temp": 150,
          "precipitation": 0,
          "weather_station_id": "STATION1",
          "ingestion_timestamp": "2023-01-01T00:00:00"
        }
      ]
    }
    ```
  - `400 Bad Request`: Invalid date format or illogical date.
    ```json
    {
      "error": "Invalid date format or illogical date. Use YYYY-MM-DD format."
    }
    ```
  - `404 Not Found`: No records matching the criteria.
    ```json
    {
      "error": "No records matching this criteria found."
    }
    ```

### `/api/weather/stats`
- **Description**: Retrieve weather statistics.
- **Method**: `GET`
- **Parameters**:
  - `page` (optional): Page number for pagination (integer).
  - `per_page` (optional): Number of records per page (integer).
  - `year` (optional): Filter by year in `YYYY` format (integer).
  - `station_id` (optional): Filter by station ID (string).
- **Responses**:
  - `200 OK`: Successfully retrieved weather statistics.
    ```json
    {
      "total": 1,
      "page": 1,
      "per_page": 10,
      "items": [
        {
          "id": 1,
          "year": 2023,
          "weather_station_id": "STATION1",
          "avg_max_temp": 25.0,
          "avg_min_temp": 15.0,
          "total_precipitation": 0.5
        }
      ]
    }
    ```
  - `400 Bad Request`: Invalid year format.
    ```json
    {
      "error": "Invalid year format. Use YYYY format."
    }
    ```
  - `404 Not Found`: No records matching the criteria.
    ```json
    {
      "error": "No records matching this criteria found."
    }
    ```

## Scripts

### models.py
Defines the SQLAlchemy models:
- `WeatherRecord`: Represents weather records with fields for date, temperatures, precipitation, and station ID.
- `WeatherStats`: Represents weather statistics with fields for year, average temperatures, and total precipitation.

### load_data.py
Loads weather data from `.txt` files into the SQLite database:
- Reads weather data files.
- Inserts data into the `WeatherRecord` table.
- Ensures no duplicate entries are inserted.

### calculate_statistics.py
Calculates and stores yearly weather statistics:
- Computes average maximum and minimum temperatures, and total precipitation for each weather station per year.
- Stores the results in the `WeatherStats` table.

### remove_duplicates.py
Removes duplicate weather records:
- Identifies duplicate records with the same values for all columns.
- Keeps the record with the latest ingestion timestamp.
- Deletes other duplicates and logs the operation.

### test_app.py
Contains unit tests for the API endpoints:
- Tests validation of date and year formats, ensuring `400 Bad Request` responses for invalid inputs.
- Tests responses for valid inputs and empty results, ensuring `404 Not Found` and `200 OK` statuses as appropriate.
- Verifies pagination functionality.
- Achieves more than 80% code coverage.

## Running the Tests

To run the unit tests and check code coverage:

```bash
coverage run -m unittest discover -s src -p "test_app.py"
coverage report -m
```

This project ensures robust handling and querying of weather data, with comprehensive validation and error handling, and thorough unit tests to maintain code quality.