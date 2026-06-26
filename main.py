import uvicorn
from fastapi import FastAPI


app = FastAPI()


def runserver():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=59420,
        log_level="info"
    )


if __name__ == "__main__":
    runserver()
