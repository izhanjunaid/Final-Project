FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 3000

ENV REDIS_HOST=redis

CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"]]
