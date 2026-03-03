FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY app/ ./app/

RUN pip install .

COPY alembic.ini ./

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
