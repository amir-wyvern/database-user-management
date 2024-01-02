import logging
from db import models
from db.database import get_db, engine
from db.db_user import create_user
from schemas import UserRegisterForDataBase, UserRole

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a console handler to show logs on terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Create a file handler to save logs to a file
file_handler = logging.FileHandler('database_api.log')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def init_database(admin_username, admin_password):

     if not engine.dialect.has_table(engine, "user"):
          models.Base.metadata.create_all(engine)
          logger.info('DataBase Created')
          
          user_admin = UserRegisterForDataBase(
               username= admin_username,
               password= admin_password,
               phone_number= "+98-0000000000",
               name= "Admin",
               role= UserRole.ADMIN
          )
          create_user(user_admin, get_db().__next__())
          logger.info('User Admin initialed!')
