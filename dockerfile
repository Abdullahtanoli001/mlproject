FROM python:3.11

WORKDIR /myapp

# Copy entire project
COPY . .
COPY .env .env

# Copy artifacts
COPY artifacts ./artifacts

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
