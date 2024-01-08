from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User
from schemas import TokenResponse
from config import settings
from jose import  JWTError
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def verify_client_key(client_id: str, client_secret: str):
    if client_id == 'client_id':
        return True
    if client_secret == 'client_secret':
        return True
    return False


def verify_password(plant_password: str, hashed_password: str):
    return bcrypt_context.verify(plant_password, hashed_password)


def get_password_hash(password: str):
    return bcrypt_context.hash(password)

def get_token_payload(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGRORITHM])
    except JWTError:
        return None
    return payload

async def get_user_token(username: str, user_id: int)-> TokenResponse:
    payload: dict = {"sub": username, "id": user_id}
    access_token_expiry: timedelta = timedelta(minutes= int(settings.ACCESS_TOKEN_EXPIRE_MININUTES))
    refresh_token_expiry: timedelta = timedelta(minutes= int(settings.ACCESS_TOKEN_REFRESH_MININUTES))
    access_token: str  = await create_token(data=payload, expiry= access_token_expiry)
    refresh_token:str = await create_token(data=payload, expiry= refresh_token_expiry)
    return TokenResponse(access_token=access_token,refresh_token=refresh_token,expires_in= access_token_expiry.seconds)

async def create_token(data: dict ,  expiry: timedelta):
    payload = data.copy()
    expires: datetime = datetime.utcnow() + expiry
    payload.update({"exp": expires})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGRORITHM)
