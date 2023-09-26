from flask import Flask, jsonify, request, Blueprint
from bson import ObjectId
from models.users import User

users = Blueprint('users', __name__)

@users.route('/addUser', methods=['POST'])
def add_user():
    # Extract data from the request JSON
    name = request.json['name'].lower()
    password = request.json['password']
    phone = request.json['phone']
    profile_pic = request.json['profile_pic']
    # Create a new user in the database
    user = User(name=name, profile_pic=profile_pic, phone=phone, password=password)
    user.save()
    # Return a JSON response indicating success
    return jsonify({'message': 'success', 'code': 201}), 201

@users.route('/getUsers', methods=['GET'])
def get_users():
    users = User.get_all()
    user_list = [{'id': str(u._id), 'name': u.name, 'profile_pic': u.profile_pic, 'phone': u.phone, 'registeredAt': u.registeredAt} for u in users]
    return jsonify({'users': user_list})

#get user profile by id
@users.route('/getUser/<string:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.find_by_id(ObjectId(user_id))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'user': {'name': user.name, 'profile_pic': user.profile_pic, 'phone': user.phone}})

@users.route('/login', methods=['POST'])
def login():
    # username = request.form.get('username').lower()
    # password = request.form.get('password')
    
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
    return jsonify({'user': {'name': user.name, 'profile_pic': user.profile_pic, 'phone': user.phone}, 'statusCode':201}), 201