from typing import TypeVar, Generic
from sqlalchemy.orm import Session

T = TypeVar('T')


class BaseRepository():

    @staticmethod
    def retrieve_all(db: Session, model: Generic[T],skip: int = 0, limit: int = 100):
        return db.query(model).offset(skip).limit(limit).all()

    @staticmethod
    def retrieve_by_id(db: Session, model: Generic[T], id: int):
        return db.query(model).filter(model.id == id).first()

    @staticmethod
    def insert(db: Session, payload: Generic[T]):
        db.add(payload)
        db.commit()
        db.refresh(payload)

    @staticmethod
    def update(db: Session, payload: Generic[T]):
        db.commit()
        db.refresh(payload)

    @staticmethod
    def delete(db: Session, payload: Generic[T]):
        db.delete(payload)  
        db.commit()
        
        