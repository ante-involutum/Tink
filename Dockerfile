FROM python:3.7-slim

ENV KUBENETES_ENV=production

WORKDIR /tink

COPY . /tink

EXPOSE 8003

RUN pip install fastapi uvicorn[standard] kubernetes

CMD ["uvicorn","src.main:app","--reload","--port=8003","--host=0.0.0.0" ]


