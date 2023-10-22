from random import randrange
from typing import Any

import psycopg2
from fastapi import FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from .config import settings

app = FastAPI()

try:
    print(f"Attempting to connect to {settings.db_url}")
    conn = psycopg2.connect(
        settings.db_url,
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Connected to db successfully.")
except Exception as exc:
    print("Failed to connect to db.")
    print(exc)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


my_posts = [
    {"id": 1, "title": "Title of post 1", "content": "Content of post 1"},
    {"id": 2, "title": "Dog Breeds", "content": "Labs, Daschunds, ..."},
]


def find_post(post_id: int) -> dict[str, Any] | None:
    for post in my_posts:
        if post["id"] == post_id:
            return post

    return None


def find_index_of_post(post_id: int) -> int | None:
    for i, p in enumerate(my_posts):
        if p["id"] == post_id:
            return i

    return None


@app.get("/")
def read_root() -> dict[str, Any]:
    return {"message": "hello world"}


@app.get("/posts")
def get_posts() -> dict[str, Any]:
    """Get all posts."""
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post) -> dict[str, Any]:
    """Create a new post."""

    # Create new post
    post_dict = post.model_dump()
    post_dict["id"] = randrange(3, 10000000)
    my_posts.append(post_dict)

    # Return created post
    return {"data": post_dict}


@app.get("/posts/latest")
def get_latest_post() -> dict[str, Any]:
    """Get latest post."""

    # Get post
    post = my_posts[-1]

    # Return post
    return {"data": post}


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int) -> dict[str, Any]:
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
def delete_post_by_id(post_id: int) -> Response:
    """Delete post by id."""

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


@app.put("/posts/{post_id}")
def update_post_by_id(post_id: int, post: Post) -> dict[str, Any]:
    """Update post by id."""

    # Update post
    index = find_index_of_post(post_id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found for {post_id=}",
        )

    post_dict = post.model_dump()
    post_dict["id"] = post_id
    my_posts[index] = post_dict

    # Return new post
    return {"data": post_dict}
