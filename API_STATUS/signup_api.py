from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']  # Replace 'mydatabase' with your database name
users_collection = db['users']  # Replace 'users' with your collection name


#Preflight response headers
def Preflight():
    response_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
        "Access-Control-Max-Age": "3600"
    }
    return '', 200, response_headers


@app.route('/signup', methods=['POST','OPTIONS'])
def signup():

    # Handle preflight request
    if request.method == 'OPTIONS':
        return Preflight()

    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    # Check if username or email already exists
    if users_collection.find_one({'$or': [{'username': username}, {'email': email}]}):
        return jsonify({'message': 'Username or email already exists'}), 400

    # Create a new user document
    user = {
        'username': username,
        'email': email,
        'password': password
    }

    # Insert the user document into the collection
    users_collection.insert_one(user)

    return jsonify({'message': 'User created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True,port=8000,host='0.0.0.0')
