from config import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import HTTPException ,status
from fastapi import Depends
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from schemas import UserResponse
from config import settings

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: Annotated[str, Depends(oauth_2_scheme)]):
    credential_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,detail="Could not valide user")
    
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGRORITHM])    
        username: str = payload.get("sub")
        user_id: str = payload.get("id")  
        if username is None or user_id is None:
       
            raise credential_exception
        return UserResponse(username=username,id=int(user_id))
    except JWTError:
        raise  credential_exception
    
db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[UserResponse,Depends(get_current_user)]