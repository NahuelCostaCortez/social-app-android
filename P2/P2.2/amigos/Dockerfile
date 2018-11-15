FROM python:3.6 
RUN pip install flask && pip install gunicorn 
RUN pip install flask-sqlalchemy pymysql flask-migrate 

RUN mkdir /amigos 
COPY . /amigos 
WORKDIR /amigos 

EXPOSE 5000
CMD ["/usr/local/bin/gunicorn", "-b",  "0.0.0.0:5000", "-w", "4", "lanzar:app"]
