# 1. Imports
import requests
import pandas as pd
import sqlite3
import time
from collections import Counter
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone

# 2. API Configuration
API_KEY = 'Your_API_Key'  # Replace with your OpenWeatherMap API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
API_URL = "http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

# 3. Utility Functions
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# 4. Function to convert UNIX timestamp to IST and return only time in AM/PM format
def unix_to_ist_time_am_pm(unix_timestamp):
    utc_time = datetime.utcfromtimestamp(unix_timestamp)
    ist_offset = timedelta(hours=5, minutes=30)
    ist_time = utc_time + ist_offset
    return ist_time.strftime('%I:%M %p')  # Convert to time in AM/PM format


# 5. Data Fetching Function
def fetch_weather_data(city):
    url = API_URL.format(city=city, api_key=API_KEY)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        return {
            'city': city,
            'main': data['weather'][0]['main'],
            'temp_celsius': kelvin_to_celsius(data['main']['temp']),
            'feels_like_celsius': kelvin_to_celsius(data['main']['feels_like']),
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'timestamp': data['dt'],  # UNIX timestamp
            'date': datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d')  # UTC date
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None

# 6. Database Setup
# Optionally, delete the database file
# if os.path.exists('weather_data.db'):
#     os.remove('weather_data.db')

conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Check if the table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weather'")
result = cursor.fetchone()

# Create the table if it doesn't exist
if result is None:
    cursor.execute('''CREATE TABLE weather 
        (city TEXT, main TEXT, temp_celsius REAL, feels_like_celsius REAL, 
         humidity REAL, wind_speed REAL, timestamp INTEGER, date TEXT)''')



# 7. Data Storage Function
def store_weather_data(weather_data):
    for entry in weather_data:
        cursor.execute('''INSERT INTO weather (city, main, temp_celsius, feels_like_celsius, 
                          humidity, wind_speed, timestamp, date) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (entry['city'], entry['main'], entry['temp_celsius'], entry['feels_like_celsius'], 
                          entry['humidity'], entry['wind_speed'], entry['timestamp'], entry['date']))
    conn.commit()

# 8. Data Aggregation Function (Daily Summary)
def daily_summary():
    query = "SELECT * FROM weather WHERE date = (SELECT MAX(date) FROM weather)"
    df = pd.read_sql_query(query, conn)
    
    if not df.empty:
        avg_temp = df['temp_celsius'].mean()
        max_temp = df['temp_celsius'].max()
        min_temp = df['temp_celsius'].min()
        dominant_condition = Counter(df['main']).most_common(1)[0][0]
        
        summary = {
            'average_temp': avg_temp,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'dominant_condition': dominant_condition
        }
        return summary
    else:
        return "No data for today yet."

# 9. Alert Functions
def check_thresholds(weather_data, temp_threshold=35, breach_count=2):
    breaches = 0
    for entry in weather_data:
        if entry['temp_celsius'] > temp_threshold:
            breaches += 1
            if breaches >= breach_count:
                print(f"ALERT: {entry['city']} exceeds temperature threshold for {breach_count} consecutive updates!")
                breaches = 0  # Reset after alert
        else:
            breaches = 0  # Reset if no breach

def check_weather_condition_alerts(weather_data, alert_conditions=["Rain", "Snow"]):
    for entry in weather_data:
        if entry['main'] in alert_conditions:
            print(f"ALERT: {entry['city']} is experiencing {entry['main']}.")

# 10. Visualization Function
def plot_daily_weather():
    df = pd.read_sql_query("SELECT * FROM weather", conn)

    if not df.empty:
        plt.figure(figsize=(10, 6))
        cities = df['city'].unique()
        colors = plt.colormaps['tab10']  # Get the colormap directly

        for i, city in enumerate(cities):
            city_data = df[df['city'] == city]
            # Convert timestamps to IST AM/PM format for plotting
            timestamps_ist = [unix_to_ist_time_am_pm(ts) for ts in city_data['timestamp']]
            
            # Scatter plot for each city with different colors
            plt.scatter(timestamps_ist, city_data['temp_celsius'], color=colors(i / len(cities)), label=city, s=50)

        plt.xlabel('Timestamp (IST AM/PM)')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature Trend by City')
        plt.legend()
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()  # Adjust layout to prevent overlap
        plt.show()
    else:
        print("No data available for plotting.")

# 11. Real-time Monitoring Function
def monitor_weather(interval=30):  # Default 5-minute interval
    while True:
        weather_data = [fetch_weather_data(city) for city in CITIES]
        weather_data = [entry for entry in weather_data if entry is not None]  # Filter out None entries
        store_weather_data(weather_data)  # Store data in SQLite

        df = pd.DataFrame(weather_data)
        print("\nWeather Data in Tabular Form:")
        
        # Convert the timestamp to IST AM/PM time format before printing
        df['timestamp'] = df['timestamp'].apply(unix_to_ist_time_am_pm)
        print(df)
        

        plot_daily_weather()

        check_thresholds(weather_data)  # Check for temperature threshold breaches
        check_weather_condition_alerts(weather_data)  # Check for weather condition alerts

        print(f"Data fetched and stored. Sleeping for {interval} seconds.")
        time.sleep(interval)  # Sleep for the interval duration

# 12. Main Execution
if __name__ == "__main__":
    monitor_weather(interval=30)  # Example: Monitor every 30 seconds

