FROM ubuntu:latest

RUN apt-get update && apt-get install -y git

RUN apt-get install -y python3 python3-pip sqlite3

RUN pip3 install --upgrade pip

RUN pip3 install argparse

RUN pip3 install termcolor

RUN pip3 install datetime

RUN pip3 install psutil

RUN git clone https://github.com/martingreyes/Computacion-II.git

WORKDIR /Computacion-II/final/app

# RUN python3 trivia.py  # no hace falta ya que en el repo ya esta la bd

EXPOSE 1234

CMD ["bash"]