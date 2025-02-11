FROM python:3.12-alpine

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY tests/ tests/

RUN pytest tests/

ENV PORT=8080

CMD ["python", "src/app.py"]