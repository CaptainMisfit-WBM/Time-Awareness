import requests
from flask import Flask, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# TimezoneDB API key
API_KEY = '6IOIQ2KVWMCF'

@app.route('/get_phoenix_time', methods=['GET'])
def get_phoenix_time():
    # Fetch UTC time from TimezoneDB API
    url = f"https://api.timezonedb.com/v2.1/get-time-zone?key={API_KEY}&format=json&by=zone&zone=UTC"
    response = requests.get(url)
    data = response.json()

    # Check if the request was successful
    if data['status'] == 'OK':
        # Extract the formatted UTC time (24-hour format)
        formatted_utc_time = data['formatted']
        
        # Convert the UTC time to datetime object
        utc_time_obj = datetime.strptime(formatted_utc_time, "%Y-%m-%d %H:%M:%S")
        
        # Convert UTC to Phoenix time (UTC - 7)
        phoenix_time_obj = utc_time_obj - timedelta(hours=7)
        
        # Format the Phoenix time into 12-hour format with AM/PM
        return jsonify({'phoenix_time': phoenix_time_obj.strftime("%I:%M:%S %p")})
    else:
        return jsonify({'error': 'Error fetching time'}), 500

if __name__ == '__main__':
    app.run(debug=True)