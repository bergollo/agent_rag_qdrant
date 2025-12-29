FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY ./app ./app

EXPOSE 8001

# uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]