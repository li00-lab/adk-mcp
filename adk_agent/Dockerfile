# adk_agent/Dockerfile

FROM python:3.12-slim

RUN pip install --no-cache-dir uv==0.7.13

WORKDIR /app

# ✅ Copy parent dir (root) contents into /app
COPY ../.. /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
