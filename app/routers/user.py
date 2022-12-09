from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.schemas import UserCreate, UserOut
from app.utils import hash_string


router = APIRouter(prefix="/users", tags=['Users'])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
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


@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    this_user = db.query(models.User).get(id)
    if not this_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': f'Id {id} not found'})

    return this_user


@router.get("", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    posts = db.query(models.User).all()
    return posts
