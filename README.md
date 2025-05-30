# fastapi-sqlalchemy-crud-users

This is a simple FastAPI application that uses SQLAlchemy to perform CRUD (Create, Read, Update, Delete) operations on a User table. The app uses SQLite for storage.

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite (local file-based DB)
- Pydantic (for request/response validation)
  
## Features

- Create a new user
- Read user details by ID
- Update user information
- Delete a user
- Built using FastAPI, SQLAlchemy, and SQLite

## Database
The app uses a SQLite database file called test.db. It will be created automatically in the root directory.

## Endpoints

| Method | Endpoint         | Description          |
|--------|------------------|----------------------|
| POST   | `/users/`        | Create a new user    |
| GET    | `/users/{id}`    | Get a user by ID     |
| PUT    | `/users/{id}`    | Update user by ID    |
| DELETE | `/users/{id}`    | Delete user by ID    |

