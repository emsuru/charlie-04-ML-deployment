FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y libgomp1 && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

## CMD uvicorn app:app --host 0.0.0.0 --port $PORT
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
