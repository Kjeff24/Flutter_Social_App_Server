from datetime import datetime
from bson import ObjectId
from flask import Flask
from config.db import db
import bcrypt

class User:
    def __init__(self, name, profile_pic, phone, password):
        self._id = None
        self.registeredAt = datetime.now()
        self.name = name
        self.password=password
        self.profile_pic = profile_pic
        self.phone = phone

    def save(self):
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())

        result = db.users.insert_one({
            'name': self.name,
            'profile_pic': self.profile_pic,
            'phone': self.phone,
            'password':hashed_password,
            'registeredAt': self.registeredAt
        })
        self._id = result.inserted_id
        return str(result.inserted_id)

    @staticmethod
    def get_all():
        users = []
        for user in db.users.find():
            users.append(User.from_dict(user)) 
        return users
    
    @staticmethod
    def from_dict(user_dict):
        user = User(
            user_dict['name'],
            user_dict['profile_pic'],
            user_dict['phone'],
            user_dict['password']
        )
        user._id = user_dict['_id']
        if 'registeredAt' in user_dict:
            user.registeredAt = user_dict['registeredAt']
        return user

    @staticmethod
    def find_by_id(user_id):
        user_dict = db.users.find_one({'_id': ObjectId(user_id)})
        if user_dict is None:
            return None
        return User.from_dict(user_dict)
    
    @staticmethod
    def find_by_username_and_password(username, password):
        user_dict = db.users.find_one({'name': username})
        if user_dict is None:
            return None

        hashed_password = user_dict['password']
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return User.from_dict(user_dict)
        else:
            return None
