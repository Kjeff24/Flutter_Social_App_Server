from datetime import datetime
from bson import ObjectId
from flask import Flask
from config.db import db
import bcrypt

class User:
    def __init__(self, username=None, firstname=None, lastname=None, mobile=None, birthday=None, gender=None, visibleGender=None, location=None, profile_pic=None, password=None):
        self._id = None
        self.registeredAt = datetime.now()
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.mobile = mobile
        self.birthday = birthday
        self.gender = gender
        self.visibleGender = visibleGender
        self.location = location
        self.password=password
        self.profile_pic = profile_pic

    def save(self):
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())

        result = db.users.insert_one({
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'password':hashed_password,
            'registeredAt': self.registeredAt
        })
        self._id = result.inserted_id
        return str(result.inserted_id)

    def update(self):
        hashed_password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()) if self.password else None
        update_fields = {
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'mobile': self.mobile,
            'birthday': self.birthday,
            'gender': self.gender,
            'visibleGender': self.visibleGender,
            'location': self.location,
            'profile_pic': self.profile_pic,
        }
        
        print(update_fields)

        # Only update the password if it's not None
        if hashed_password is not None:
            update_fields['password'] = hashed_password

        result = db.users.update_one(
            {'_id': self._id},
            {'$set': update_fields}
        )

        return str(result.modified_count)

    @staticmethod
    def get_all():
        users = []
        for user in db.users.find():
            users.append(User.from_dict(user)) 
        return users
    
    @staticmethod
    def from_dict(user_dict):
        user = User(
            user_dict['username'],
            user_dict['firstname'],
            user_dict['lastname'],
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
        user_dict = db.users.find_one({'username': username})
        if user_dict is None:
            return None

        hashed_password = user_dict['password']
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return User.from_dict(user_dict)
        else:
            return None
        
    @staticmethod
    def find_by_username(username):
        user_dict = db.users.find_one({'username': username})
        if user_dict is None:
            return None
        return User.from_dict(user_dict)
