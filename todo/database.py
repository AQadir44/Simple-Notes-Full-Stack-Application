# database.py

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://todo_db_owner:uGmrQH2W9vTU@ep-divine-bonus-a52mlcod.us-east-2.aws.neon.tech/todo_db?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL , pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
    
