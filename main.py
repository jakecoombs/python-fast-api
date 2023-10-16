from random import randrange

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


my_posts = [
    {"id": 1, "title": "Title of post 1", "content": "Content of post 1"},
    {"id": 2, "title": "Dog Breeds", "content": "Labs, Daschunds, ..."},
]


@app.get("/")
def read_root():
    return {"message": "hello world"}


@app.get("/posts")
def get_posts():
    """Get all posts."""
    return {"data": my_posts}


@app.post("/posts")
def create_post(post: Post):
    """Create a new post."""

    # Create new post
    post_dict = post.model_dump()
    post_dict["id"] = randrange(3, 10000000)
    my_posts.append(post_dict)

    # Return created post
    return {"data": post_dict}
