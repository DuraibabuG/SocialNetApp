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
   git clone https://github.com/yourusername/social-network-api.git
   cd social-network-api
   Create and activate a virtual environment:
   ```

bash
Copy code
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Configure the database:
or you can install all using pip install

you can go on admine also frist create superuser - 

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
python manage.py migrate
Create a superuser:

bash
Copy code
python manage.py createsuperuser
Run the development server:

bash
Copy code
python manage.py runserver
API Endpoints
User Signup
URL: /api/signup/
Method: POST
Request:
json
Copy code
{
"email": "user@example.com",
"username": "username",
"password": "password",
"first_name": "First",
"last_name": "Last"
}
Response:
json
Copy code
{
"user": {
"id": 1,
"email": "user@example.com",
"username": "username",
"first_name": "First",
"last_name": "Last"
},
"refresh": "refresh_token",
"access": "access_token"
}
User Login
URL: /api/token/
Method: POST
Request:
json
Copy code
{
"email": "user@example.com",
"password": "password"
}
Response:
json
Copy code
{
"refresh": "refresh_token",
"access": "access_token"
}
Search Users
URL: /api/search/
Method: GET
Request: ?q=search_query
Response:
json
Copy code
[
{
"id": 1,
"email": "user@example.com",
"username": "username",
"first_name": "First",
"last_name": "Last"
}
]
Send Friend Request
URL: /api/friend-request/send/
Method: POST
Request:
json
Copy code
{
"to_user_id": 2
}
Response:
json
Copy code
{
"message": "Friend request sent"
}
Accept/Reject Friend Request
URL: /api/friend-request/action/
Method: POST
Request:
json
Copy code
{
"request_id": 1,
"action": "accept" # or "reject"
}
Response:
json
Copy code
{
"message": "Friend request accepted"
}
List Friends
URL: /api/friends/
Method: GET
Response:
json
Copy code
[
{
"id": 2,
"email": "friend@example.com",
"username": "friend",
"first_name": "Friend",
"last_name": "User"
}
]
List Pending Friend Requests
URL: /api/friend-requests/pending/
Method: GET
Response:
json
Copy code
[
{
"id": 1,
"from_user": {
"id": 1,
"email": "user@example.com",
"username": "username",
"first_name": "First",
"last_name": "Last"
},
"to_user": {
"id": 2,
"email": "friend@example.com",
"username": "friend",
"first_name": "Friend",
"last_name": "User"
},
"status": "pending",
"timestamp": "2024-01-01T12:00:00Z"
}
]


#Contributed BY - SANDEEP TALE
