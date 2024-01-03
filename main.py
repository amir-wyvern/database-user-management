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

        except Exception as e:
        
            logging.error(f'error [fn: NewUser err_msg: {e}')

            return pb2.BaseResponse(**{'message': 'failed' , 'code': 1400})


        return pb2.BaseResponse(**{'message': 'success' , 'code': 1200})


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

