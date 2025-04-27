from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ Allow Cross-Origin for frontend
import pickle
import numpy as np
from pymongo import MongoClient  # ✅ New for MongoDB
import hashlib  # ✅ New for password hashing

# Create Flask app
app = Flask(__name__)
CORS(app)

# Load the trained model
try:
    with open('flight_price_model.pkl', 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    raise Exception("Model file not found. Please check the filename and path!")

# Connect to MongoDB Atlas
client = MongoClient('mongodb+srv://nnm22ad049:nu22l67@cluster0.btyhg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['sharanya']  # database name
users_collection = db['cluster0']  # collection name

# Utility function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Registration API
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    # Check if user already exists
    if users_collection.find_one({'username': username}):
        return jsonify({'message': 'Username already exists'}), 409

    # Insert user with hashed password
    users_collection.insert_one({
        'username': username,
        'password': hash_password(password)
    })
    return jsonify({'message': 'Registration successful'}), 201

# Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = users_collection.find_one({'username': username})

    if user and user['password'] == hash_password(password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Prediction API (already there)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        if 'duration' not in data or 'days_left' not in data:
            return jsonify({'error': 'Missing input: duration and days_left are required.'}), 400

        duration = data['duration']
        days_left = data['days_left']

        input_features = np.array([[duration, days_left]])
        prediction = model.predict(input_features)

        return jsonify({'predicted_price': round(prediction[0], 2)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run app
if __name__ == '__main__':
    app.run(debug=True)
