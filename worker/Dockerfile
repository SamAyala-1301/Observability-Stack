FROM python:3.10.18-slim
WORKDIR /worker
COPY worker.py .
RUN pip install psycopg2-binary
CMD ["python", "worker.py"]