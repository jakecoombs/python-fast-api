from random import randrange

from fastapi import FastAPI, HTTPException, Response, status
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


def find_post(post_id: int):
    for post in my_posts:
        if post["id"] == post_id:
            return post


def find_index_of_post(post_id: int):
    for i, p in enumerate(my_posts):
        if p["id"] == post_id:
            return i


@app.get("/")
def read_root():
    return {"message": "hello world"}


@app.get("/posts")
def get_posts():
    """Get all posts."""
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    """Create a new post."""

    # Create new post
    post_dict = post.model_dump()
    post_dict["id"] = randrange(3, 10000000)
    my_posts.append(post_dict)

    # Return created post
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post():
    """Get latest post."""

    # Get post
    post = my_posts[-1]

    # Return post
    return {"data": post}


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int):
    """Get post by id."""

    # Get post
    post = find_post(post_id)

    # Return 404 if not found
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found for {post_id=}",
        )

    # Return post
    return {"data": post}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(post_id: int):
    """Delete post by id."""

    print("DELETING")

    # Delete post
    index = find_index_of_post(post_id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found for {post_id=}",
        )

    my_posts.pop(index)

    # Return success message
    return Response(status_code=status.HTTP_204_NO_CONTENT)
