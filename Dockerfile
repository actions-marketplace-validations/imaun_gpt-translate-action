FROM python:3.9

WORKDIR /app

COPY translate.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/app/translate.py"]