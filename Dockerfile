FROM python:3.6.8-jessie

RUN apt-get -y update && apt-get -y upgrade 
RUN apt-get install -y apt-utils redis-server 
ENV MYSQL_PWD root
RUN echo "mysql-server mysql-server/root_password password $MYSQL_PWD" | debconf-set-selections \
 && echo "mysql-server mysql-server/root_password_again password $MYSQL_PWD" | debconf-set-selections \
 && apt-get install -y mysql-server

VOLUME ["/opt/homework/MiMarket"]

RUN mkdir -p /opt/homework/MiMarket
WORKDIR /opt/homework/MiMarket
COPY ./requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY ["./Control","./Db","./Redis","./static","./templates","./View","./main.py", "./"]

EXPOSE 23334

RUN python, "/opt/homework/MiMarket/main.py"
CMD ["python", "/opt/homework/MiMarket/main.py"]
