# FastAPI for User and Article Management
This project is the server-side component of a web application that provides an API for managing Users and Articles. It utilizes the FastAPI framework for building the API endpoints and stores data in a PostgreSQL database. Additionally, it implements JWT-based security for authentication.
## Technologies Used

*  Backend: FastAPI.
*  Database: Async PostgreSQL.
*  Docker for containerization.


## Installing / Getting started:
```shell
To get started, you need to clone the repository from GitHub: https://github.com/Morty67/users_and_articles/tree/developer
Python 3.11.3 must be installed

python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)

pip install -r requirements.txt

alembic upgrade head
uvicorn app.main:app --reload

```

## How to get access
Domain:
*  localhost:8000 or 127.0.0.1:8000 (127.0.0.1:8000/docs)

## Run Docker 🐳
Docker must be installed :
docker-compose up --build
```shell


## Features:
*  Save User: Create or update a user in the database.
*  Save Article: Create or update an article in the database.
*  Get Users by Age: Retrieve all users whose age is greater than a specified value.
*  Get Users with Articles by Color: Retrieve all users who have articles with a specific color (enum value).
*  Get Unique User Names with More Than 3 Articles: Retrieve unique user names of users who have more than 3 articles. (тут про лише залогіненим користувачам)
*  This project implements JWT-based authentication for securing API endpoints. To access protected endpoints, users must obtain a valid JWT token by following the authentication process.
*  API documentation is available at http://localhost:8000/docs when the application is running. You can explore and test the endpoints using the Swagger UI.


## Curl Requests for Postman

### Create User
curl -X POST "http://127.0.0.1:8000/users/create_user/" -H "Content-Type: application/json" -d '{
  "name": "Hello World123",
  "age": 67
}'

### Create Article
curl -X POST "http://127.0.0.1:8000/articles/create_article/" -H "Content-Type: application/json" -d '{
  "text": "string",
  "color": "red",
  "owner_name": "Hello"
}'

### Users Older Than
curl -X GET "http://127.0.0.1:8000/users/users_older_than/?age_threshold=30"

### Users By Color
curl -X GET "http://127.0.0.1:8000/users/users_by_color/?color=red"

### Create Profile
curl -X POST "http://127.0.0.1:8000/profiles/create_profile/" -H "Content-Type: application/json" -d '{
  "username": "HelloTest4",
  "email": "test4@example.com",
  "full_name": "string",
  "hashed_password": "string"
}'
### Login
curl -X POST "http://127.0.0.1:8000/profiles/login" -d "username=HelloTest4&password=string"

### Users With More Than 3 Articles
curl -X GET "http://127.0.0.1:8000/users/users_with_more_than_3_articles/" -H "Authorization: Bearer <YOUR TOKEN>"

### Current User Profile
curl -X GET "http://127.0.0.1:8000/profiles/users/me" -H "Authorization: Bearer <YOUR TOKEN>"
