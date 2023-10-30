from fastapi import HTTPException, Depends, status, Request, Cookie, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from database import SessionLocal
from models.models import UserTable
from utils import verify_jwt_token

db= SessionLocal()
reuseable_oauth = OAuth2PasswordBearer(tokenUrl='/api/Account/SignIn')

async def get_current_user(token: str = Depends(reuseable_oauth)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_jwt_token(token)
        if payload is not None:
            username :str = payload['sub']
        if payload is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(UserTable).filter(UserTable.username == payload['sub']).first()
    if user is None:
        raise credentials_exception
    return user

