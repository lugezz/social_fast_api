from sqlalchemy import Boolean, Column, DateTime, func, Integer, String

from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE")
    created_at = Column(DateTime(), default=func.now())
