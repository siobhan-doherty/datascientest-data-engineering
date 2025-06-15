FROM python:3.9-slim

WORKDIR /my_server/

COPY server.py .

# Using compatible versions
RUN pip install flask==2.0.0 werkzeug==2.0.3

EXPOSE 5000

CMD ["python", "server.py"]
