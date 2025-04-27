import requests
import json

# Define the URL for the POST request
url = 'http://127.0.0.1:5000/predict'

# Create the data (as a dictionary)
data = {
    "duration": 120,
    "days_left": 30
}

# Send POST request to Flask app
response = requests.post(url, json=data)

# Print the server response (predicted price)
if response.status_code == 200:
    result = response.json()
    print("Predicted Price:", result.get('predicted_price'))
else:
    print("Error:", response.text)
