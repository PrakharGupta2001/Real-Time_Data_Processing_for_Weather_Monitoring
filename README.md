# Weather Monitoring System

This Python application fetches real-time weather data for various Indian cities using the OpenWeatherMap API, stores the data in an SQLite database, generates visualizations, and sends alerts based on configurable thresholds.

## Features
- Fetches real-time weather data for multiple cities.
- Stores data persistently in an SQLite database.
- Generates daily summaries (average, max, min temperatures, dominant weather condition).
- Provides visualizations of temperature trends.
- Triggers alerts when specific weather conditions (e.g., rain) are detected.
- Alerts if temperature exceeds a threshold for consecutive updates.
- Configurable interval for fetching weather data.
- Runs as a Docker container for easy deployment.

## Requirements

To run the application, you need:
- Python 3.x
- An OpenWeatherMap API key (sign up at https://openweathermap.org/)
- Docker (optional for containerized deployment)

## Installation and Setup

### 1. Clone the repository:

```bash
git clone https://github.com/your-username/weather-monitoring.git
cd weather-monitoring
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure API Key:

```bash
set API_KEY=your_openweather_api_key
```

### 4. Running the Application Locally:

```bash
python weather_monitor.py
```

## Running the Application with Docker

You can run the entire application inside a Docker container.

### 1. Build the Docker Image:

In the project directory, run:
```bash
docker build -t weather-monitor .
```

### 2. Run the Docker Container:

You can run the container and pass the OpenWeatherMap API key as an environment variable:
```bash
docker run -e API_KEY=your_openweather_api_key weather-monitor
```
This will launch the application inside a Docker container.

## Configuration

You can configure the following:

### Interval: 
Modify the interval for fetching weather data in the monitor_weather function (default is 30 seconds).
### Temperature Threshold: 
Adjust the threshold in the check_thresholds function.
### Weather Alerts: 
Customize weather condition alerts in check_weather_condition_alerts (e.g., for "Rain" or "Snow").

## File Structure

```bash
.
├── Dockerfile
├── README.md
├── requirements.txt
├── weather_monitor.py
└── weather_data.db  # SQLite database file (created when the script runs)
```

## Troubleshooting
### API Key Error: 
Make sure your OpenWeatherMap API key is correctly set.
### Database Issues: 
Ensure the weather_data.db file is writable and not corrupted.
### Docker Issues: 
Verify that Docker is installed and running.
