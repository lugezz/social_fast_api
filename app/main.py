from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models
from .schemas import Post, PostCreate, UserCreate, UserOut
from .utils import hash_string


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World my old friend"}


@app.get("/posts", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # Easiest way unpacking the post dictionary
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.get("/posts/latest", response_model=Post)
def get_latest(db: Session = Depends(get_db)):
    this_post = db.query(models.Post).order_by(desc(models.Post.id)).first()

    return this_post


@app.get("/posts/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    this_post = db.query(models.Post).get(id)
    if not this_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    return this_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    to_delete_post = db.query(models.Post).filter(models.Post.id == id)

    if not to_delete_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    to_delete_post.delete(synchronize_session=False)
    db.commit()

    return to_delete_post


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    this_post = db.query(models.Post).filter(models.Post.id == id)

    if not this_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    print(post.dict())
    this_post.update(values=post.dict(), synchronize_session=False)
    db.commit()

    return f"Post {this_post.first().title} updated"

# ------ USERS -----------------------------------------------------------------


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email is used
    this_email_count = db.query(models.User).filter(models.User.email == user.email).count()

    if this_email_count > 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email already used")

    # Hash the password
    user.password = hash_string(user.password)
    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    this_user = db.query(models.User).get(id)
    if not this_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    return this_user


@app.get("/users", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    return posts
