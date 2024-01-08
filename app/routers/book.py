from fastapi import APIRouter, status
from schemas import Response, BookCreate, BookUpdate
from controller import book
from models import Book
from dependencies import db_dependency, user_dependency

router = APIRouter(prefix="/book", tags=["book"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book_service(request: BookCreate, db: db_dependency, user: user_dependency):
    book.create_book(db, book=request, user=user)
    return Response(message="Book created successfully").dict(exclude_none=True)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_books(skip: int = 0, limit: int = 100, db: db_dependency = None):
    _books: list[Book] = book.get_books(db, skip, limit)
    return Response(message="Success fetch all data", result=_books)


@router.get("/{book_id}", status_code=status.HTTP_200_OK)
async def get_books_by_id(book_id: int, db: db_dependency):
    _book: Book = book.get_book_by_id(db, book_id=book_id)
    return Response(message="Success fetch all data", result=_book)


@router.patch("/", status_code=status.HTTP_200_OK)
async def update_book(request: BookUpdate, db: db_dependency):
    _book: Book = book.get_book_by_id(db, request.id)
    if not _book:
        return Response(message="This book id doesn't exist").dict(exclude_none=True)
    _book: Book = book.update_book(db, book=_book,
                                   title=request.title, description=request.description,)
    return Response(message="Success update data", result=_book)


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int,  db: db_dependency):
    _book: Book = book.get_book_by_id(db, book_id)
    if not _book:
        return Response(message="This book id doesn't exist").dict(exclude_none=True)
    book.delete_book(db=db, book=_book)
    return Response(message="Success delete data").dict(exclude_none=True)
