import grpc 
from concurrent import futures
import grpc_utils.database_pb2_grpc as pb2_grpc
import grpc_utils.database_pb2 as pb2
import logging
from db.inital import init_database
from db.database import get_db
from schemas import UserRegisterForDataBase
import os

from db import db_user

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

PORT = os.getenv("GRPC_PORT")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

if PORT.isdigit():
    PORT = int(PORT)

else:
    logger.error(f'Port is not useable! [port: {PORT}]')
    exit(0)
    

class DataBaseService(pb2_grpc.DataBaseServicer):

     def GetUser(self, request, context):

        try:
            user = db_user.get_user_by_username(request.username ,get_db().__next__())

            if user is None:

                return pb2.BaseResponse(**{'message': 'username not exist' , 'code': 1401})
            
            user_data = {
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'phone_number': user.phone_number,
                'role': user.role
            } 
            return pb2.BaseResponse(**{'message': 'success' , 'code': 1200, 'data': user_data})


        except Exception as e:
        
            logging.error(f'error [fn: GetUser err_msg: {e}')

            return pb2.BaseResponse(**{'message': 'failed' , 'code': 1400})


     def NewUser(self, request, context):

        receive_data = {
            'name': request.name,
            'username': request.username,
            'password': request.password,
            'phone_number': request.phone_number,
            'email': request.email,
            'role': request.role
        }
        try:
        
            db_user.create_user(UserRegisterForDataBase(**receive_data) ,get_db().__next__())
            logging.info(f'create user was successfully [username: {request.username}]')

            return pb2.BaseResponse(**{'message': 'success' , 'code': 1200})
        
        except Exception as e:
        
            logging.error(f'error [fn: NewUser err_msg: {e}')

            return pb2.BaseResponse(**{'message': 'failed' , 'code': 1400})


     def ModifyUserPassword(self, request, context):

        try:
            user = db_user.get_user_by_username(request.username ,get_db().__next__())

            if user is None:

                return pb2.BaseResponse(**{'message': 'username not exist' ,'code': 1401})
            
            db_user.update_password(user.user_id, request.password ,get_db().__next__())
            logging.info(f'user password updated successfully [username: {request.username}]')

            return pb2.BaseResponse(**{'message': 'success' ,'code': 1200})
        
        except Exception as e:
        
            logging.error(f'error [fn: ModifyUserPassword err_msg: {e}')

            return pb2.BaseResponse(**{'message': 'failed' ,'code': 1400})

     
     def ModifyUserInfo(self, request, context):

        try:
            user = db_user.get_user_by_username(request.username ,get_db().__next__())

            if user is None:

                return pb2.BaseResponse(**{'message': 'username not exist' ,'code': 1401})
            
            if not any([request.name, request.email, request.phone_number]):
            
                return pb2.BaseResponse(**{'message': 'There is no field to update' ,'code': 1402})
                
            if request.name:
                db_user.update_name(user.user_id, request.password ,get_db().__next__(), commit= False)
            
            if request.email:
                db_user.update_email(user.user_id, request.email ,get_db().__next__(), commit= False)
            
            if request.phone_number:
                db_user.update_phone_number(user.user_id, request.phone_number ,get_db().__next__(), commit= False)

            get_db().__next__().commit()

            logging.info(f'user info updated successfully [username: {request.username}]')

            return pb2.BaseResponse(**{'message': 'success' ,'code': 1200})
        
        except Exception as e:
        
            logging.error(f'error [fn: ModifyUserPassword err_msg: {e}')

            return pb2.BaseResponse(**{'message': 'failed' ,'code': 1400})

     

def serve():

    try:

        init_database(ADMIN_USERNAME, ADMIN_PASSWORD)

        logger.info(f'service grpc database is runing [::]:{PORT} ...')

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        pb2_grpc.add_DataBaseServicer_to_server(DataBaseService(), server)
        server.add_insecure_port(f'[::]:{PORT}')
        server.start()
        server.wait_for_termination()

    except Exception as e:
        
        logger.error(f'occure error: [{e}]')
        exit(0)
         
serve()

