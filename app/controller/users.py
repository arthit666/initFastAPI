from repository.users import UsersRepository
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from controller.auth import get_password_hash


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return UsersRepository.retrieve_all(db=db, model=User, skip=skip, limit=limit)


def get_user_by_id(db: Session, user_id: int) -> User:
    return UsersRepository.retrieve_by_id(db=db, model=User, id=user_id)


def create_user(db: Session, user: UserCreate) -> None:
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username,
                    hashed_password=hashed_password,
                    email=user.email,
                    full_name=user.full_name,
                    )

    return UsersRepository.insert(db=db, payload=new_user)
