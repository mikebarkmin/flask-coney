FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=main.py

CMD [ "flask" , "run" , "--host=0.0.0.0" ]
