FROM python:3.11-slim

WORKDIR /app


COPY requirements/requirements.txt /app/requirements/
RUN pip install -r requirements/requirements.txt

COPY . .

WORKDIR /app/src

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
