from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.oauth2 import creat_access_token
from app.schemas import UserLogin
from app.utils import verify_password


router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    this_user = db.query(User).filter(User.email == user_credentials.email).first()

    if not this_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': 'Invalid credentials'})

    ok_password = verify_password(user_credentials.password, this_user.password)

    if not ok_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'message': 'Invalid credentials'})

    access_token = creat_access_token(data={'user_id': this_user.id})
    resp = {
        'access_token': access_token,
        'token_type': 'bearer'
    }

    return resp
