# Todo_list

A simple todo list with a Python backend that uses FastAPI and sqlite database and an Angular Frontend.

## Frontend
The todo list has essentially two pages. One page for login in as a user and then the page that lists the todo tasks. 

The todo tasks can be added, edited and removed.

## Backend
The backend has a basic swagger UI showing how to use the backend API, and some basic tests that test the functionality

## How to start
To start the project first edit the `docker-compose.yml` found in the root with the correct ip address for the backend API.
Unless the port forwarding is changed, the port for the Backend should be `3000`. Do not add a slash at then of the api url.

Then run: 

```sh
docker compose -f docker-compose.yml up --build
```

The frontend should be accessible at `http://<ipaddres>:4000/` and the Swagger UI for the backend at `http://<ipaddres>:3000/`

## Limitations
As I am not that familiar with frontend frameworks, I had to learn angular from scratch. There are no tests for the frontend.


## API Requests/Responses

### POST: /user
This is to create a user just with a username. Returns the userId of the user created.

Request Body:
```json
{
  "username": "string"
}
```
Response:
```json
1
```


### GET: /user
This is to get the user_id given a username. Returns the user id of the user.

Request url:
```
/user/?username=andrew
```
Response:
```json
1
```


### GET: /user/user_id/notes
Get all the notes that a user has created. Returns a list of notes

Request url:
```
/user/1/notes
```
Response:
```json
[
  {
    "id": 5,
    "user_id": 1,
    "title": "string",
    "body": "string"
  }
]
```

### POST: /todo/
Create a todo note for a user. Returns the json object of the note created

Request body:
```json
{
  "user_id": 1,
  "title": "string",
  "body": "string"
}
```
Response:
```json
{
  "id": 5,
  "user_id": 1,
  "title": "string",
  "body": "string"
}

```


### GET: /todo/{todo_id}
Get a specific note based on the notes id. Returns the note 

Request url:
```
/todo/5
```
Response:
```json
{
  "id": 5,
  "user_id": 1,
  "title": "string",
  "body": "string"
}
```


### PUT: /todo/{todo_id}
Update a specific note. Returns the updated note

Request url:
```
/todo/5
```
Request Body
```json
{
  "title": "Hello",
  "body": "World"
}
```

Response:
```json
{
  "id": 5,
  "user_id": 1,
  "title": "Hello",
  "body": "World"
}
```


### DELETE: /todo/{todo_id}
Delete a specific note. Returns the note deleted

Request url:
```
/todo/5
```
Response:
```json
{
  "id": 5,
  "user_id": 1,
  "title": "Hello",
  "body": "World"
}
```