import uvicorn
import os



# file to programatically start fastapi

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.environ['APP_HOSTNAME'],
        port=int(os.environ['APP_PORT']),
    )