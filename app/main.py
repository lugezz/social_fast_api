from fastapi import Depends, FastAPI, HTTPException, status

from pydantic import BaseModel
from sqlalchemy import desc
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


@app.get("/")
def root():
    return {"message": "Hello World my old friend - Cachulengo"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return {"Data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # Easiest way unpacking the post dictionary
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {'new_post': new_post}


@app.get("/posts/latest")
def get_latest(db: Session = Depends(get_db)):
    this_post = db.query(models.Post).order_by(desc(models.Post.id)).first()

    return {"Data": this_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    this_post = db.query(models.Post).get(id)
    if not this_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    return {"Data": this_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    to_delete_post = db.query(models.Post).filter(models.Post.id == id)

    if not to_delete_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    to_delete_post.delete(synchronize_session=False)
    db.commit()

    return {"Data": f"Post {id} deleted"}


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    this_post = db.query(models.Post).filter(models.Post.id == id)

    if not this_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    print(post.dict())
    this_post.update(values=post.dict(), synchronize_session=False)
    db.commit()

    return {"Data": f"Post {this_post.first().title} updated"}
