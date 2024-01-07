from schemas import UserRegisterForDataBase, UserRole
from db.database import get_db, engine, inspect
from passlib.context import CryptContext
from db.db_user import create_user
from db import models
import logging 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_database(admin_username: str, admin_password: str, logger: logging):

     if not inspect(engine).has_table("user"):
          models.Base.metadata.create_all(engine)
          logger.info('DataBase Created')
          
          user_admin = UserRegisterForDataBase(
               username= admin_username,
               password= pwd_context.hash(admin_password),
               phone_number= "+98-0000000000",
               name= "Admin",
               role= UserRole.ADMIN
          )
          create_user(user_admin, get_db().__next__())
          logger.info('User Admin initialed!')
