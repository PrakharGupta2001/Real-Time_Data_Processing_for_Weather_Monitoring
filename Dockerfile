# 1. Use an official Python runtime as a parent image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the current directory contents into the container at /app
COPY . /app

# 4. Install any necessary dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Set environment variables
ENV API_KEY=your_api_key_here

# 6. Run the script when the container launches
CMD ["python", "weather_monitor.py"]
