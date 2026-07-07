FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY backend/config.py .

# Expose API port
EXPOSE 5000

# Create data directory
RUN mkdir -p data

# Run the Flask app
CMD ["python", "app/main.py"]
