# Flask and MongoDB RESTful API for [Flutter_Social_App](https://github.com/Kjeff24/Flutter_Social_App.git)

## Introduction

This documentation provides an overview and usage guide for the Flask and MongoDB-based RESTful API.

### Prerequisites

Before using this API, make sure you have the following installed:

- Python
- Flask
- pymongo (Python MongoDB driver)
- MongoDB
- Install the required dependencies: 
```
pip install -r requirements.txt
```
- Setup Database uri. Get uri from cloud or use local server. You can use a `.env` file to store it or change it from `db.py`. For example:

```
DATABASE_URI = 'mongodb+srv://<username>>:<password>@cluster0.qf1qitd.mongodb.net/'
```

### API Base URL

The base URL for accessing the API is `http://127.0.0.1:5000`.  NB: <span style="color: #4ff6ff">Some routes have been defined with a common url prefix (`url_prefix`), check it out in `app.py`. Include url prefix to the base url before including the endpoints</span>

## Endpoints

### Add a New User

- **URL**: `/addUser`
- **HTTP Method**: POST
- **Request Body**: JSON data representing the new user.
- **Response**:
  - HTTP Status: 201 (Created)
  - JSON Response:
    ```
    {
        'message': 'success', 'code': 201
    }
    ```

### Retrieve All Users

- **URL**: `/getUsers`
- **HTTP Method**: GET
- **Response**:
  - HTTP Status: 200 (OK)
  - JSON Response:
    ```
    {
        'users': user_list
    }
    ```

### Retrieve a User by ID

- **URL**: `/getUser/<string:user_id>`
- **HTTP Method**: GET
- **Response**:
  - HTTP Status: 200 (OK)
  - JSON Response:
    ```
    {
        'user': {'name': user.name, 'profile_pic': user.profile_pic, 'phone': user.phone}
    }
    ```
  - HTTP Status: 404 (Not Found)
  - JSON Response (if item with ID not found):
    ```
    {
        'error': 'User not found'
    }
    ```

### Login a User

- **URL**: `/login`
- **HTTP Method**: POST
- **Request Body**: JSON data representing user login credentials.
- **Response**:
  - HTTP Status: 200 (OK)
  - JSON Response:
    ```
    {
        'user': {'name': user.name, 'profile_pic': user.profile_pic, 'phone': user.phone}
    }
    ```
  - HTTP Status: 404 (Not Found)
  - JSON Response (if user credentials not found):
    ```
    {
        'error': 'User not found'
    }
    ```


## Example Usage

Here are some examples of how to use the API:

### Get a response from login

```bash
curl -X POST http://127.0.0.1:5000/users/login -H "Content-Type: application/json" -d '{"field1": "value1", "field2": "value2"}'
