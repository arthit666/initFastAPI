from sqlalchemy.orm import Session
from repository.book import BookRepository
from models import Book, User
from schemas import BookCreate


def get_books(db: Session, skip: int = 0, limit: int = 100) -> list[Book]:
    return BookRepository.retrieve_all(db=db, model=Book, skip=skip, limit=limit)


def get_book_by_id(db: Session, book_id: int) -> Book:
    return BookRepository.retrieve_by_id(db=db, model=Book, id=book_id)


def create_book(db: Session, book: BookCreate, user: User) -> None:
    _book = Book(title=book.title,
                 description=book.description, author_id=user.id)
    return BookRepository.insert(db=db, payload=_book)


def delete_book(db: Session, book:  Book)-> None:
    BookRepository.delete(db=db, payload=book)


def update_book(db: Session, book: BookCreate, title: str, description: str) -> Book:
    book.title = title
    book.description = description
    BookRepository.update(db=db, payload=book)
    return book


