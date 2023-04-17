FROM ubuntu:latest

RUN apt-get update && apt-get install -y git

RUN apt-get install -y python3 python3-pip sqlite3

RUN pip3 install --upgrade pip

RUN pip3 install argparse

RUN pip3 install termcolor

RUN pip3 install datetime

RUN pip3 install psutil

RUN git clone https://github.com/martingreyes/Computacion-II.git

WORKDIR /Computacion-II/final

RUN git pull

RUN python3 trivia.py

EXPOSE 1234

CMD ["bash"]

# MACHETE COMANDOS

# docker build -t compu2 .

# 	docker run -it -p 1234:1234 compu2

# 	docker run -it compu2

# git clone https://github.com/martingreyes/Computacion-II.git

# git pull

# python3 trivia.py

# python3 server.py -p 1234

# python3 cliente.py -d 127.0.0.1 -p 1234 -ip 4

# python3 cliente.py -d ::1 -p 1234 -ip 6