from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.oauth2 import create_access_token
from app.schemas import Token
from app.utils import verify_password


router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    this_user = db.query(User).filter(User.email == user_credentials.username).first()

    if not this_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail={'message': 'Invalid credentials'})

    ok_password = verify_password(user_credentials.password, this_user.password)

    if not ok_password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail={'message': 'Invalid credentials'})

    access_token = create_access_token(data={'user_id': this_user.id})
    resp = {
        'access_token': access_token,
        'token_type': 'bearer'
    }

    return resp
