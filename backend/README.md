docker build -f Dockerfile -t todo_backend:latest .
docker run -p 8000:8000 todo_backend:latest