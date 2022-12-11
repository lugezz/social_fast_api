from datetime import datetime, timedelta

from jose import jwt

from app.config import my_config


"""
We need 3 things:
- Secret Key
- Algorithm
- Expiration time
"""

SECRET_KEY = my_config['secret_key']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def creat_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode['exp'] = expire

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
