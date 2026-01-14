FROM python:3.12.3-slim

WORKDIR /

COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY accounts/. .

EXPOSE 50051

CMD ["python", "main.py"]
