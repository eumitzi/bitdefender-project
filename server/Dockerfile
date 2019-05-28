# docker build --no-cache --network=host -t flask --file Dockerfile .
FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "flask", "run" ]