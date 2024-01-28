from flask import Flask
import requests
import time
from datetime import datetime, timedelta

app = Flask(__name__)

bitcoin_values_service_a = []
bitcoin_values_service_b = []

def get_bitcoin_value():
    bitcoin_api_url = 'https://api.coinbase.com/v2/prices/BTC-USD/buy'
    
    try:
        response = requests.get(bitcoin_api_url)
        if response.status_code == 200:
            data = response.json().get('data', {})
            amount = float(data.get('amount', 0))
            return amount
        else:
            print(f"Error: Unable to fetch bitcoin value. HTTP Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error: {str(e)}")

def print_average_value(service_values, service_name):
    if service_values:
        average_value = sum(service_values) / len(service_values)
        timestamp = datetime.utcnow().strftime('%y-%m-%d %H:%M UTC')
        result = f"{service_name}, average bitcoin value is {average_value:.2f}$ for '{timestamp}'"
        return result
        service_values.clear()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/ServiceA')
def service_a_endpoint():
    bitcoin_value = get_bitcoin_value()
    
    if bitcoin_value is not None:
        timestamp = datetime.utcnow().strftime('%y-%m-%d %H:%M UTC')
        data = f"Service A, bitcoin value is {bitcoin_value:.2f}$ for '{timestamp}'"
        bitcoin_values_service_a.append(bitcoin_value)

        if len(bitcoin_values_service_a) == 10:
            result = print_average_value(bitcoin_values_service_a, "Service A")
            return result

        return data
    else:
        return "Failed to fetch bitcoin value for Service A"

@app.route('/ServiceB')
def service_b_endpoint():
    bitcoin_value = get_bitcoin_value()
    
    if bitcoin_value is not None:
        timestamp = datetime.utcnow().strftime('%y-%m-%d %H:%M UTC')
        data = f"Service B, bitcoin value is {bitcoin_value:.2f}$ for '{timestamp}'"
        bitcoin_values_service_b.append(bitcoin_value)

        if len(bitcoin_values_service_b) == 10:
            result = print_average_value(bitcoin_values_service_b, "Service B")
            return result

        return data
    else:
        return "Failed to fetch bitcoin value for Service B"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

