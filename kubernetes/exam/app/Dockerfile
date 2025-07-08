FROM ubuntu:20.04

# copy code & install OS deps + Python
ADD requirements.txt main.py ./
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip libmysqlclient-dev \
 && pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:server", "--host", "0.0.0.0", "--port", "8000"]
