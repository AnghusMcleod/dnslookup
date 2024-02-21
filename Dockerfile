# Dockerfile
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5000

CMD ["python", "dnslookup.py"]
