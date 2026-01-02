FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
ENV PYTHONUNBUFFERED=1

# EXPOSE 8002
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]

# Cloud Run
# Optional: Cloud Run doesn’t require EXPOSE, but it’s fine to set 8080 for clarity
EXPOSE 8080
# Use PORT if set, else default to 8080
CMD exec uvicorn app.main:app --host 0.0.0.0 --port 8080

