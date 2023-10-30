from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Response,Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse

from deps import get_current_user
from deps import db
from models.models import UserTable
from schemas import Userout, Usercr
from utils import create_refresh_token, create_access_token, verify_password, get_hashed_password

authusers = APIRouter(prefix="/api/Account",
    tags=["AccountController"],
    responses={404: {"description": "Not found"}})

@authusers.get('/Me', response_model=Userout)
async def meuser(user:UserTable = Depends(get_current_user)):
    # response.headers['Authorization'] =
   return user


@authusers.post('/SignIn')
async def login(request:Request,form_data:OAuth2PasswordRequestForm = Depends()):
    users = db.query(UserTable).filter(UserTable.username == form_data.username).first()
    if not db.query(UserTable).filter(UserTable.username == form_data.username).all():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    hash_pasw = users.password
    if not verify_password(form_data.password,hash_pasw):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(users.username)
    request.session["access_token"] = 'Bearer ',access_token
    return {"access_token":access_token,
        'refresh_token':create_refresh_token(users.username),
        "token_type":'Bearer'}

@authusers.post('/SignUp',response_model=Userout)
async def signup(user: Usercr):
    if db.query(UserTable).filter(UserTable.username == user.username).all():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail='User with this username already exist'
        )
    user = UserTable(
        username = user.username,
        password = get_hashed_password(user.password),
    )
    db.add(user)
    db.commit()
    return user

@authusers.post('/SignOut')
async def logout (user = Depends(get_current_user)):
    return RedirectResponse("/")


@authusers.put('/Update',response_model=Userout)
async def update_user(username:str,password:str,user = Depends(get_current_user)):
    if db.query(UserTable).filter(UserTable.username == username).all():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail='User with this username already exist'
        )
    user1 = db.query(UserTable).filter(UserTable.username == user.username).first()
    user1.username = username
    user1.password = get_hashed_password(password)
    db.add(user1)
    db.commit()
    return user1
