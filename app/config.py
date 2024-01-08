from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class Settings():
    DB_USER: str = os.getenv('POSTGRES_USER')
    DB_PASSWORD: str = os.getenv('POSTGRES_PASSWORD')
    DB_NAME: str = os.getenv('POSTGRES_DB')
    DB_HOST: str = os.getenv('POSTGRES_SERVER')
    DB_PORT: str = os.getenv('POSTGRES_PORT')
    DATABASE_URL: str = os.getenv('POSTGRES_URL')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGRORITHM: str = os.getenv('ALGRORITHM')
    ACCESS_TOKEN_EXPIRE_MININUTES: str = os.getenv('ACCESS_TOKEN_EXPIRE_MININUTES')
    ACCESS_TOKEN_REFRESH_MININUTES: str = os.getenv('ACCESS_TOKEN_REFRESH_MININUTES')
    
def get_settings():
    return Settings()

settings = get_settings()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine)
Base = declarative_base()