from flask import Flask
from routes.users import users
from routes.posts import posts

app = Flask(__name__)
app.debug = True 
# Register the users blueprint
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(posts, url_prefix='/posts')
#display message on the browser when the server is running
@app.route('/')
def route():
    return 'running!'

if __name__ == '__main__':
    app.run(host="0.0.0.0")
    # app.run(host="0.0.0.0", port=5000, debug=True)