from datetime import datetime
from typing import Any

import psycopg2
from fastapi import Depends, FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, TypeAdapter
from sqlalchemy.orm import Session

from . import models
from .config import settings
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

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
    created_at: datetime | None = None

    class Config:
        from_attributes = True


@app.get("/")
def read_root() -> dict[str, Any]:
    return {"message": "hello world"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)) -> dict[str, Any]:
    """Get all posts."""

    # Fetch all posts
    results = db.query(models.Posts).all()

    return {"data": TypeAdapter(list[Post]).validate_python(results)}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post) -> dict[str, Any]:
    """Create a new post."""

    # Create new post
    cursor.execute(
        """
        INSERT INTO posts (title, content, published)
        VALUES (%s, %s, %s)
        RETURNING *
    """,
        (
            post.title,
            post.content,
            post.published,
        ),
    )
    created_post = cursor.fetchone()
    conn.commit()

    # Return created post
    return {"data": created_post}


@app.get("/posts/latest")
def get_latest_post() -> dict[str, Any]:
    """Get latest post."""

    # Get latest created post
    cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1""")
    post = cursor.fetchone()

    # Return post
    return {"data": post}


@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int) -> dict[str, Any]:
    """Get post by id."""

    # Get post
    cursor.execute("""SELECT * FROM posts WHERE id=%s""", (post_id,))
    post = cursor.fetchone()

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
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (post_id,))
    deleted_post = cursor.fetchone()

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found for {post_id=}",
        )

    conn.commit()

    # Return success message
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{post_id}")
def update_post_by_id(post_id: int, post: Post) -> dict[str, Any]:
    """Update post by id."""

    # Update post
    cursor.execute(
        """
            UPDATE posts
            SET title=%s, content=%s, published=%s 
            WHERE id=%s 
            RETURNING *
        """,
        (post.title, post.content, post.published, post_id),
    )
    updated_post = cursor.fetchone()

    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post not found for {post_id=}",
        )

    conn.commit()

    # Return new post
    return {"data": updated_post}
