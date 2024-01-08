from fastapi import APIRouter, HTTPException ,status, Depends
from schemas import TokenResponse
from fastapi.security import  OAuth2PasswordRequestForm
from typing import Annotated
from dependencies import db_dependency
from controller import auth ,users
from models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token",response_model=TokenResponse)
async def token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], db: db_dependency):
    user: User = auth.authenticate_user(db=db,username=form_data.username,password=form_data.password)
    if not user:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user")
    token = auth.get_user_token(user.username,user.id)
    return TokenResponse(access_token=token).dict()
    

@router.post("/login", response_model=TokenResponse)
async def login(form_data: Annotated[OAuth2PasswordRequestForm,Depends()], db: db_dependency):
  
    user: User = auth.authenticate_user(db=db,username=form_data.username,password=form_data.password)
    if not user:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user")
   
    # if not auth.verify_client_key(form_data.client_id,form_data.client_secret):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate client key")
    
    return await auth.get_user_token(username=user.username,user_id=user.id)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_token: str , db: db_dependency):
    payload = auth.get_token_payload(token=refresh_token)
    if not payload:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token or expires")
    user_id = payload.get("id", None)
    user: User = users.get_user_by_id(db, user_id)
    if not user:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate user")
    return await auth.get_user_token(username=user.username,user_id=user.id)