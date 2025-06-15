import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",          # The import string for your FastAPI app
        host="127.0.0.1",    # The IP address to bind to
        port=8000,           # The port to listen on
        reload=True          # Enable auto-reloading for development
    )