# database.py

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.config import Config
from starlette.datastructures import Secret

SQLALCHEMY_DATABASE_URL= Config("SQLALCHEMY_DATABASE_URL", cast=Secret)

engine = create_engine(SQLALCHEMY_DATABASE_URL , pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
    
