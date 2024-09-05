FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

ENV FLASK_ENV=production

CMD ["python", "main.py"]
