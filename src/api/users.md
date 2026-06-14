Users API

The Users API provides endpoints for managing user accounts.

Features

* Create User
* Retrieve User
* Update User
* Delete User

Endpoints

Create User

Method: POST

Path:

/api/users

Get User

Method: GET

Path:

/api/users/{id}

Update User

Method: PUT

Path:

/api/users/{id}

Delete User

Method: DELETE

Path:

/api/users/{id}

Authentication

All Users API endpoints require a valid authentication token.

Response Format

All endpoints return JSON responses with:

* Success status
* Message
* Data payload
* Error details (when applicable)