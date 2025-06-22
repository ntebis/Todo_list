# Todo_list

A simple todo list with a Python backend that uses FastAPI and sqlite database and an Angular Frontend.

## Frontend
The todo list has essentially two pages. One page for login in as a user and then the page that lists the todo tasks. 

The todo tasks can be added, edited and removed.

## Backend
The backend has a basic swagger UI showing how to use the backend API

## How to start
To start the project first edit the `docker-compose.yml` found in the root with the correct ip address.

Then run: 

`docker compose -f docker-compose.yml up --build`
