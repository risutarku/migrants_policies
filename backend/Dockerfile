FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/src /app/backend/src

ENV PYTHONPATH=/app/backend/src

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
