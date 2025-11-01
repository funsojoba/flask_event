FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for psycopg2 and geospatial libs
RUN apt-get update && apt-get install -y \
    libpq-dev gcc g++ postgis \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]