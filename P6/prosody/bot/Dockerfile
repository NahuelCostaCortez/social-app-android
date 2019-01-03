FROM python:3.6
RUN pip install wheel sleekxmpp

RUN mkdir /bot
COPY . /bot
WORKDIR /bot

EXPOSE 5000

CMD python MiBotContenedor.py
