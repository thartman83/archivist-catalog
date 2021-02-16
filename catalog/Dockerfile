FROM python:3.8-alpine
WORKDIR /app
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
RUN apk add --no-cache gcc musl-dev linux-headers zlib-dev jpeg-dev mariadb-dev build-base
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]
