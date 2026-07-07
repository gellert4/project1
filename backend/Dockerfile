FROM python:3.10-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app

# Expose API port
EXPOSE 5000

# Run the Flask app
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
