# docker build --no-cache -t flask --file Dockerfile .
FROM python:3

WORKDIR /usr/src/app

# . = currdir
# copy src dest -> copy . (de pe primul sistem / server) . (de pe al doilea / workdir) 
COPY . . 

RUN pip install -e . 
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000:5000/tcp
CMD [ "flask", "run", "--host", "0.0.0.0"]
