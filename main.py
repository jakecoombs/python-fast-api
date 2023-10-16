from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "hello world"}


@app.get("/posts")
def get_posts():
    return {"data": {"posts": [{"id": 1, "message": "first post"}]}}
