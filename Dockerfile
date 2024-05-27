FROM python:latest

COPY . .

RUN pip install -r ./requirements.txt
EXPOSE 8000

WORKDIR /app

CMD ["python", "main.py"]