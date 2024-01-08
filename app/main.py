from fastapi import FastAPI
import models
from routers import book, users, auth
from config import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(book.router)
app.include_router(users.router)
app.include_router(auth.router)


