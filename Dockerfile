FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the local code to the container
COPY main.py .
Copy requirements.txt .
COPY schemas.py .
COPY db/ ./db
COPY grpc_utils/ ./grpc_utils

RUN pip install --upgrade -r requirements.txt

CMD ["python", "./main.py"]
