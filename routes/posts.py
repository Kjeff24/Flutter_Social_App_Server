from flask import jsonify, request, Blueprint
from models.posts import Post

from config.db import db

posts = Blueprint('posts', __name__)

@posts.route('/addPost', methods=['POST'])
def add_post():
    post = Post()
    for key, value in request.json.items():
        if hasattr(post, key):
            setattr(post, key, value)
    post.save()
    
    return jsonify({'message': 'success', 'code': 201}), 201

@posts.route('/getPosts', methods=['GET'])
def get_posts():
    # Use the get_all method to retrieve all posts
    all_posts = Post.get_all()

    # Convert each post to a dictionary and then to JSON
    return jsonify([post.to_dict() for post in all_posts])


@posts.route('/getPostsByUser/<string:user_id>', methods=['GET'])
def get_posts_by_user(user_id):
    # Use the get_by_user_id method to retrieve all posts by the user
    user_posts = Post.get_by_user_id(user_id)
    if not user_posts:
        return jsonify({'error': 'Posts not found'}), 404
    # Convert each post to a dictionary and then to JSON
    return jsonify({"message": "success", "data": [post.to_dict() for post in user_posts]})
