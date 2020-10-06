FROM ubuntu:latest


LABEL Author="Ivan Zilic"
LABEL E-mail="ivan.zilic9@gmail.com"
LABEL version="0.0.1"


# Install python3
RUN apt-get update
RUN apt-get install -y python3.7 python3-pip


RUN mkdir -p /weboscket/socket_io

WORKDIR /weboscket/socket_io

# Copy requirements.txt
COPY requirements.txt .

# Copy my socket main
COPY . .

#ADD run_socket_app/run_socket_app.py .

# Install dependencies
RUN pip3 install -r requirements.txt

# Expost port
EXPOSE 5000

# Set default directory
ENV HOME /weboscket/socket_io

#ENV PYTHONPATH "${PYTONPATH}: /weboscket/socket_io"



# run gunicorn & eventlent worker

CMD ["gunicorn", "run_socket_app:app", "--worker-class",  "eventlet", "-w",  "1",  "-b", "0.0.0.0:5000", "--reload"]
