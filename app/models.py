from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Posts(Base):
    __tablename__ = "posts"

    post_id: Mapped[int] = mapped_column("id", primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    published: Mapped[bool] = mapped_column(default=True)
    created_at = mapped_column(
        TIMESTAMP(timezone=True), server_default=text("NOW()")
    )
