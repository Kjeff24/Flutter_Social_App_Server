from flask import Flask
from routes.users import users

app = Flask(__name__)
# app.debug = True 
# Register the users blueprint
app.register_blueprint(users, url_prefix='/users')
#display message on the browser when the server is running
@app.route('/')
def route():
    return 'running!'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)