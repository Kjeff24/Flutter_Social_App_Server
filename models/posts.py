from datetime import datetime
from config.db import db
from models.users import User
from bson import ObjectId

class Post:
    def __init__(self, message=None, image=None, likes=None, ownerId=None):
        self._id = None
        self.date = datetime.now()
        self.message = message
        self.image = image
        self.likes = likes
        self.ownerId = ownerId
        self.owner = None
        
    
    def save(self):
        owner = User.find_by_id(self.ownerId)  # Retrieve the User object
        if owner is None:
            raise ValueError("User with ownerId not found")

        self.owner = owner  # Assign the User object, not the owner_dict

        result = db.posts.insert_one({
            'message': self.message,
            'image': self.image,
            'likes': self.likes,
            'date': self.date,
            'owner': self.owner.to_dict()  # Save owner as a dictionary if needed
        })
        self._id = result.inserted_id

        
    def to_dict(self):
        return {
            'id': str(self._id),
            'message': self.message,
            'image': self.image,
            'likes': self.likes,
            'owner': self.owner.to_dict() if self.owner else None
        }

        
    @staticmethod
    def get_all():
        posts = []
        for post in db.posts.find():
            posts.append(Post.from_dict(post)) 
        return posts
    
    @staticmethod
    def from_dict(post_dict):
        post = Post(
            message=post_dict['message'],
            image=post_dict['image'],
            likes=post_dict['likes'],
            ownerId=post_dict['owner']['_id']
        )
        post._id = post_dict['_id']
        if 'date' in post_dict:
            post.date = post_dict['date']
        # You can also create a User object for the owner here if needed
        post.owner = User.from_dict(post_dict['owner'])
        return post
    
    
    @staticmethod
    def get_by_user_id(user_id):
        posts = []
        for post in db.posts.find({'owner._id': user_id}):
            posts.append(Post.from_dict(post))
        if not posts:
            return None
        return posts
