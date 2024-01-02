from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base() 

sessionlocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    session = sessionlocal()
    try:
        yield session
    finally:
        session.close()

