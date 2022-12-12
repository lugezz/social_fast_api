from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.oauth2 import get_current_user
from app.schemas import Post, PostCreate


router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # Easiest way unpacking the post dictionary
    new_post = models.Post(**post.dict())
    new_post.owner_id = current_user.id

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/latest", response_model=Post)
def get_latest(db: Session = Depends(get_db)):
    this_post = db.query(models.Post).order_by(desc(models.Post.id)).first()

    return this_post


@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    this_post = db.query(models.Post).get(id)
    if not this_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    return this_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    to_delete_post = db.query(models.Post).filter(models.Post.id == id)

    if not to_delete_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    to_delete_post.delete(synchronize_session=False)
    db.commit()

    return to_delete_post


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    this_post = db.query(models.Post).filter(models.Post.id == id)

    if not this_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    this_post.update(values=post.dict(), synchronize_session=False)
    db.commit()

    return this_post.first()
