from sqlalchemy import  Column, Integer, String , DateTime, ForeignKey
from sqlalchemy.orm import  relationship, Mapped, mapped_column
from config import Base
import datetime


class User(Base):
    __tablename__ ="users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    full_name = Column(String)
    email = Column(String)
    create_date = Column(DateTime,default= datetime.datetime.utcnow)
    
    books : Mapped[list["Book"]] = relationship()
    
    def __repr__(self):
        return f"<User({self.username})>"

class Book(Base):
    __tablename__ ="books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id")) 
     
    author: Mapped[User] = relationship(back_populates= "books")
    
    def __repr__(self):
        return f"<Book({self.title})>"
    
     

    
  
    