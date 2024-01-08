from fastapi import APIRouter, status
from schemas import Response, UserCreate, UserResponse, BookResponse
from controller import users
from models import User
from dependencies import db_dependency

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(skip: int = 0, limit: int = 100, db: db_dependency = None):
    _users: list[User] = users.get_users(db=db, skip=skip, limit=limit)

    user_res: list[UserResponse] = []
    for user in _users:
        book_res: list[BookResponse] = []
        for book in user.books:
            book_res.append(BookResponse(id=book.id,title=book.title,description=book.description))
        user_res.append(UserResponse(id=user.id,
                                     username=user.username,
                                     full_name=user.full_name,
                                     email=user.email,
                                     books=book_res,
                                     ))

    return Response(message="Success fetch all data", result=user_res)


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db: db_dependency):
    _user: User = users.get_user_by_id(db, user_id)
    return Response(message="Success fetch all data", result=_user)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate, db: db_dependency):
    users.create_user(db=db, user=user_create)
    return Response(message="Create User").dict(exclude_none=True)
