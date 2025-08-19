FROM python:3.13.7-alpine3.21

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src .

CMD ["fastapi", "run", "/app/main.py", "--port", "80"]
