# Social Network API

This is a social networking API built with Django Rest Framework. The API provides functionalities for user signup, login,
searching users, sending/accepting/rejecting friend requests, listing friends, and viewing pending friend requests.

# Features

- User Signup
- User Login
- Search User by Email/Name
- Send Friend Request
- Accept/Reject Friend Request
- List Friends
- List Pending Friend Requests
- Rate limiting on sending friend requests

  # Requirements

- Python 3.10+
- Django 4.2+
- Django Rest Framework 3.14+
- sql lite

  # Installation
  
1. **Clone the repository:**

   ```bash
   git clone https://github.com/DuraibabuG/SocialNetApp.git
   cd SocialNetApp
   Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate # On Windows use `.\venv\Scripts\activate`
  ```

# Install the dependencies:
pip install -r requirements.txt

# Configure the database:
or you can install all using pip install

Update the DATABASES setting in settings.py with your database configuration.

python
Copy code
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'your_db_name',
'USER': 'your_db_user',
'PASSWORD': 'your_db_password',
'HOST': 'localhost',
'PORT': '5432',
}
}
Apply migrations:

bash
Copy code
cd SocialNetApp
python manage.py migrate

# Run the development server:

bash
python manage.py runserver
# To view api 127.0.0.1:8000/swagger/
# API Endpoints
## User Signup
URL: /authapi/sign_up/
Method: POST
Request:
json
{
  "first_name": "First",
  "last_name": "Last",
  "email": "user@example.com",
  "is_active": true,
  "date_joined": "2024-06-07T16:53:35.365Z",
  "password": "password",
  "gender": "M" #/"F"
}

Response:
json
{
  "user_info": {
    "id": 13,
    "email": "user@example.com",
    "first_name": "First",
    "last_name": "Last",
    "gender": "M"
  },
  "token": "access_token"  # Authenticate using this token by following format without "" - "Token access_token" 
}

## User Login
URL: /authapi/login/
Method: POST
Request:
json
{
"email": "user@example.com",
"password": "password"
}
Response:
json
{
  "info": "userinfo", # to view use base64 decription
  "token": "access_token" # use this token to authenticate
}

## Search Users
URL: /authapi/search_user/
Method: POST
Request: {
  "req_data": "string"
}
Response:
json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "first_name": "First",
      "last_name": "Last",
      "email": "user@example.com",
      "id": 13
    }
  ]
}

## Send Friend Request
URL: /authapi/friend_request_send/
Method: POST
Request:
json
{
  "to_user_id": 2
}
Response:
json
{
  "message": "Friend request sent"
}

## Accept/Reject Friend Request
URL: /authapi/frien_request_action/
Method: POST
Request:
json
{
  "request_id": 1,
  "action": "accept"  # or "reject"
}
Response:
json
{
  "message": "Friend request accepted"
}

## List Friends
URL: /authapi/friends_list/
Method: GET
Response:
json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "first_name": "Akilan",
      "last_name": "H",
      "email": "akilanh@example.com",
      "id": 7
    }
  ]
}

## List Pending Friend Requests
URL: /authapi/friend_requests_pending/
Method: GET
Response:
json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "status": "pending",
      "created_at": "2024-06-06T18:42:19.228239Z",
      "from_user": 9,
      "to_user": 13
    }
  ]
}


# Contributed BY - DURAIBABU G
