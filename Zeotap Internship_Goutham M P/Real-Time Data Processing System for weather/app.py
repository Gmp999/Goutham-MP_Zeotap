from flask import Flask, render_template, jsonify
import requests
import threading
import time
import sqlite3
from datetime import datetime

app = Flask(__name__)

# OpenWeatherMap API key and configuration
API_KEY = "a8fdb404c4ded7d1a81cadf0e84c6cf7"
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
weather_data = {}
alert_thresholds = {'temperature': 35}  # Example alert threshold
alert_log = []

# Database setup for daily summaries
def init_db():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            date TEXT,
            avg_temp REAL,
            max_temp REAL,
            min_temp REAL,
            dominant_condition TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            message TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_weather_data():
    global weather_data
    while True:
        for city in CITIES:
            response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric")
            if response.status_code == 200:
                data = response.json()
                weather_data[city] = {
                    'main': data['weather'][0]['main'],
                    'temp': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'dt': datetime.utcfromtimestamp(data['dt']).strftime('%d %B %Y, %I:%M %p')  # Human-readable format
                }
                check_alerts(city, weather_data[city]['temp'])
        time.sleep(300)

def check_alerts(city, temperature):
    if temperature > alert_thresholds['temperature']:
        message = f'Alert: {city} temperature exceeded {alert_thresholds["temperature"]}°C'
        timestamp = datetime.utcnow().strftime('%d %B %Y, %I:%M %p')  # Human-readable format
        alert_log.append({'city': city, 'message': message, 'timestamp': timestamp})
        save_alert_to_db(city, message, timestamp)

def save_alert_to_db(city, message, timestamp):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO alerts (city, message, timestamp) VALUES (?, ?, ?)', (city, message, timestamp))
    conn.commit()
    conn.close()

def aggregate_daily_data():
    while True:
        time.sleep(86400)  # Run this once a day
        conn = sqlite3.connect('weather_data.db')
        c = conn.cursor()
        for city in CITIES:
            temps = [weather_data[city]['temp'] for _ in range(5)]  # Example: mock data for 5 readings
            avg_temp = sum(temps) / len(temps)
            max_temp = max(temps)
            min_temp = min(temps)
            dominant_condition = weather_data[city]['main']
            date = datetime.utcnow().strftime('%d %B %Y')  # Human-readable format
            c.execute('''
                INSERT INTO daily_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (city, date, avg_temp, max_temp, min_temp, dominant_condition))
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/weather')
def weather():
    return jsonify(weather_data)

@app.route('/alerts')
def alerts():
    return jsonify(alert_log)

@app.route('/daily_summary')
def daily_summary():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM daily_summary')
    summaries = c.fetchall()
    conn.close()
    return jsonify(summaries)

if __name__ == '__main__':
    init_db()
    threading.Thread(target=fetch_weather_data, daemon=True).start()
    threading.Thread(target=aggregate_daily_data, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=True)
