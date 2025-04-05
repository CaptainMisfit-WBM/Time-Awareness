from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

API_KEY = '6IOIQ2KVWMCF'

@app.route('/get_phoenix_time', methods=['GET'])
def get_phoenix_time():
    try:
        url = f"https://api.timezonedb.com/v2.1/get-time-zone?key={API_KEY}&format=json&by=zone&zone=UTC"
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'OK':
            formatted_utc_time = data['formatted']
            utc_time_obj = datetime.strptime(formatted_utc_time, "%Y-%m-%d %H:%M:%S")
            phoenix_time_obj = utc_time_obj - timedelta(hours=7)
            return jsonify({'phoenix_time': phoenix_time_obj.strftime("%I:%M:%S %p")})
        else:
            return jsonify({'error': 'Invalid response from API'}), 502
    except Exception as e:
        return jsonify({'error': str(e)}), 500