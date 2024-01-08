# from dotenv import load_dotenv
import os

# load_dotenv()

import grpc_utils.database_pb2_grpc as pb2_grpc
from schemas import UserRegisterForDataBase
from passlib.context import CryptContext
import grpc_utils.database_pb2 as pb2
from db.inital import init_database
from concurrent import futures
from db.database import get_db
from db import db_user
import logging
import grpc 


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create a console handler to show logs on terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Create a file handler to save logs to a file
file_handler = logging.FileHandler('database_api.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

PORT = os.getenv("GRPC_PORT")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

map_enums = {
    0 : 'ADMIN',
    1 : 'USER'
}

if PORT.isdigit():
    PORT = int(PORT)

else:
    logger.error(f'Port is not useable! [port: {PORT}]')
    exit(0)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DataBaseService(pb2_grpc.DataBaseServicer):

     def GetUser(self, request, context):

        logging.debug(f'[GetUser] Receive a Requests [username: {request.username}]')
        db = get_db().__next__()
        try:
            user = db_user.get_user_by_username(request.username, db)
            print()
            if user is None:
                logging.debug(f'[GetUser] Username Not Found [username: {request.username}]')
                return pb2.ResponseUserInfo(**{'message': 'Username Not Found' , 'code': 1401})
            
            user_data = {
                'username': user.username,
                'password': user.password,
                'name': user.name,
                'email': user.email,
                'phone_number': user.phone_number,
                'role': user.role
            } 

            return pb2.ResponseUserInfo(**{'message': 'success' , 'code': 1200, 'data': user_data})


        except Exception as e:
        
            logging.error(f'[GetUser] occure an error [error: {e}]')
            return pb2.ResponseUserInfo(**{'message': 'Exception in database service (check the logs for more detail)' , 'code': 1405})


     def NewUser(self, request, context):
    
        logging.debug(f'[NewUser] Receive a Requests [username: {request.username}]')
        db = get_db().__next__()

        try:
            
            user = db_user.get_user_by_username(request.username, db)

            if user:
                logging.debug(f'[NewUser] Username already exists [username: {request.username}]')
                return pb2.BaseResponse(**{'message': 'Username already exist' , 'code': 1403})
            
            if request.email and db_user.get_user_by_email(request.email, db):
                logging.debug(f'[NewUser] Email already exists [username: {request.username} -email: {request.email}]')
                return pb2.BaseResponse(**{'message': 'Email already exist' , 'code': 1406})
            
            if db_user.get_user_by_phone_number(request.phone_number, db):
                logging.debug(f'[NewUser] PhoneNumber already exists [username: {request.username} -phone_number: {request.phone_number}]')
                return pb2.BaseResponse(**{'message': 'PhoneNumber already exists' , 'code': 1407})

            receive_data = {
                'name': request.name,
                'username': request.username,
                'password': pwd_context.hash(request.password),
                'phone_number': request.phone_number,
                'role': map_enums[request.role]
            }

            if request.email:
                receive_data.update({'email': request.email})

            db_user.create_user(UserRegisterForDataBase(**receive_data) ,db)
            logging.info(f'[NewUser] create user was successfully [username: {request.username}]')

            return pb2.BaseResponse(**{'message': 'success' , 'code': 1200})
        
        except Exception as e:
        
            logging.error(f'[NewUser] occure an error [error: {e}]')
            return pb2.BaseResponse(**{'message': 'Exception in database service (check the logs for more detail)' , 'code': 1405})


     def ModifyUserPassword(self, request, context):

        logging.debug(f'[ModifyUserPassword] Receive a Requests [username: {request.username}]')
        db = get_db().__next__()

        try:
            user = db_user.get_user_by_username(request.username, db)

            if user is None:
                logging.debug(f'[ModifyUserPassword] Username Not Found [username: {request.username}]')
                return pb2.BaseResponse(**{'message': 'Username Not Found' ,'code': 1401})
            
            db_user.update_password(user.user_id, pwd_context.hash(request.password), db)
            logging.info(f'[ModifyUserPassword] user password updated successfully [username: {request.username}]')

            return pb2.BaseResponse(**{'message': 'success' ,'code': 1200})
        
        except Exception as e:
        
            logging.error(f'[ModifyUserPassword] occure an error [error: {e}]')
            return pb2.BaseResponse(**{'message': 'Exception in database service (check the logs for more detail)' ,'code': 1405})

     
     def ModifyUserInfo(self, request, context):

        logging.debug(f'[ModifyUserInfo] Receive a Requests [username: {request.username}]')
        db = get_db().__next__()

        try:
            user = db_user.get_user_by_username(request.username, db)

            if user is None:
                logging.debug(f'[ModifyUserInfo] Username Not Found [username: {request.username}]')
                return pb2.BaseResponse(**{'message': 'Username Not Found' ,'code': 1401})
            
            if not any([request.name, request.email, request.phone_number]):
                logging.debug(f'[ModifyUserInfo] There is no field to update [username: {request.username}]')
                return pb2.BaseResponse(**{'message': 'There is no field to update' ,'code': 1402})

            if request.name:
                db_user.update_name(user.user_id, request.name, db, commit= False)

            if request.email:
                if db_user.get_user_by_email(request.email, db):
                    
                    db.rollback()
                    logging.debug(f'[ModifyUserInfo] Email already exists [username: {request.username} -email: {request.email}]')
                    return pb2.BaseResponse(**{'message': 'Email already exist' , 'code': 1406})
                
                db_user.update_email(user.user_id, request.email ,db, commit= False)
            
            if request.phone_number:
                if db_user.get_user_by_phone_number(request.phone_number, db):
                    
                    db.rollback()
                    logging.debug(f'[ModifyUserInfo] PhoneNumber already exists [username: {request.username} -phone_number: {request.phone_number}]')
                    return pb2.BaseResponse(**{'message': 'PhoneNumber already exist' , 'code': 1407})
                
                db_user.update_phone_number(user.user_id, request.phone_number, db, commit= False)

            db.commit()
            logging.info(f'[ModifyUserInfo] Username info updated successfully [username: {request.username}]')

            return pb2.BaseResponse(**{'message': 'success' ,'code': 1200})
        
        except Exception as e:
        
            logging.error(f'[ModifyUserInfo] occure an error [error: {e}]')
            return pb2.BaseResponse(**{'message': 'Exception in database service (check the logs for more detail)' ,'code': 1405})
        
        
     def ModifyUserRole(self, request, context):

        logging.debug(f'[ModifyUserRole] Receive a Requests [username: {request.username}]')
        db = get_db().__next__()

        try:
            user = db_user.get_user_by_username(request.username, db)

            if user is None:
                logging.debug(f'[ModifyUserRole] Username Not Found [username: {request.username}]')
                return pb2.BaseResponse(**{'message': 'Username Not Found' ,'code': 1401})
            
            db_user.update_role(user.user_id, map_enums[request.role], db)
            logging.info(f'[ModifyUserRole] Username role updated successfully [username: {request.username} -new_role: {request.role}]')

            return pb2.BaseResponse(**{'message': 'success' ,'code': 1200})
        
        except Exception as e:
        
            logging.error(f'[ModifyUserRole] occure an error [error: {e}]')
            return pb2.BaseResponse(**{'message': 'Exception in database service (check the logs for more detail)' ,'code': 1405})


     def DeleteUser(self, request, context):

        logging.debug(f'[DeleteUser] Receive a Requests [username: {request.username}]')
        db = get_db().__next__()

        try:
            user = db_user.get_user_by_username(request.username, db)

            if user is None:
                logging.debug(f'[DeleteUser] Username Not Found [username: {request.username}]')
                return pb2.BaseResponse(**{'message': 'Username Not Found' ,'code': 1401})
            
            db_user.delete_user(user.user_id, db)
            logging.debug(f'[DeleteUser] Username deleted successfully [username: {request.username}]')

            return pb2.BaseResponse(**{'message': 'success' ,'code': 1200})
        
        except Exception as e:
        
            logging.error(f'[DeleteUser] occure an error [error: {e}]')
            return pb2.BaseResponse(**{'message': 'Exception in database service (check the logs for more detail)' ,'code': 1405})


def serve():

    try:

        init_database(ADMIN_USERNAME, ADMIN_PASSWORD, logger)

        logger.info(f'service grpc database is runing [::]:{PORT} ...')

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_DataBaseServicer_to_server(DataBaseService(), server)
        server.add_insecure_port(f'[::]:{PORT}')
        server.start()
        server.wait_for_termination()

    except Exception as e:
        
        logger.error(f'Occure error: [{e}]')
        exit(0)
         
serve()

