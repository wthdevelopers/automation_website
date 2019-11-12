FROM python:3.8.0-alpine3.10

WORKDIR /usr/src/backendapp

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY . .

CMD [ "python3", "./wsgi.py" ]
