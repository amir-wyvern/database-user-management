from db.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum
)

class DbUser(Base):

    __tablename__ = 'user'

    user_id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    name = Column(String(50), index=True, nullable=False)
    phone_number = Column(String(20), index=True, unique=True, nullable=False)
    email = Column(String(100), index=True, unique=True, nullable=True)
    username = Column(String(100), index=True, nullable=False, unique= True)
    password = Column(String(100), nullable=False) 
