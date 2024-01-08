from typing import  Optional,TypeVar
from pydantic import BaseModel 

T = TypeVar('T')


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int
    
class TokenRefresh(BaseModel):
    refresh_token: str
    
    
class Response(BaseModel):
    message: str
    result: Optional[T]
    
class BookBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    id: int
    pass

class BookResponse(BookBase):
    id: int
    author: object
    
    class Config():
        orm_mode = True

class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    
class UserCreate(UserBase):
    password: str    
    
class UserResponse(UserBase):
    id: int
    books: list[BookResponse] = []
    
    class Config:
        orm_mode = True