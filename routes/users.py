from flask import jsonify, request, Blueprint
from bson import ObjectId
from models.users import User
import jwt 
import os

# Define a secret key for JWT (replace with your own secret key)
SECRET_KEY = os.environ.get('SECRET_KEY')


users = Blueprint('users', __name__)

@users.route('/addUser', methods=['POST'])
def add_user():
    # Extract data from the request JSON
    username = request.json['username'].lower()
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    password = request.json['password']
    
    # Check if a user with the same username already exists
    existing_user = User.find_by_username(username)
    if existing_user is not None:
        return jsonify({'message': 'A user with this username already exists', 'code': 400}), 400
    
    # Create a new user in the database
    user = User(username=username, firstname=firstname, lastname=lastname, password=password)
    user.save()
    
    # Generate a JWT token
    
    # Return a JSON response indicating success
    return jsonify({'message': 'success', 'code': 201}), 201

@users.route('/getUsers', methods=['GET'])
def get_users():
    users = User.get_all()
    user_list = [{'id': str(u._id), 'username': u.username, 'firstname': u.firstname, 'lastname': u.lastname, 'registeredAt': u.registeredAt} for u in users]
    return jsonify({'users': user_list})

#get user profile by id
@users.route('/getUser/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.find_by_id(ObjectId(user_id))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': {'id': str(user._id),'username': user.username, 'firstname': user.firstname, 'lastname': user.lastname}})

@users.route('/login', methods=['POST'])
def login():
    
    data = request.json

    if not data:
        return jsonify({'error': 'JSON data is required'}), 400

    username = data.get('username', '').lower()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Your authentication and validation logic goes here
    user = User.find_by_username_and_password(username,password)

    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    token = jwt.encode({'username': username}, SECRET_KEY, algorithm='HS256')
    return jsonify({'data': {'id': str(user._id), 'username': user.username, 'firstname': user.firstname, 'lastname': user.lastname, 'token': token}}), 200

@users.route('/update/<string:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.find_by_id(ObjectId(user_id))
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if a user with the same username already exists
    if request.json['username'].lower():
        existing_user = User.find_by_username(request.json['username'].lower())
    if existing_user is not None:
        return jsonify({'message': 'A user with this username already exists', 'code': 400}), 400

    # Iterate over the keys and values in the request JSON
    for key, value in request.json.items():
        if hasattr(user, key):
            setattr(user, key, value)

    result = user.update()

    return jsonify({'modified_count': result})