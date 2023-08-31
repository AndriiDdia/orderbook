FROM python:3.11

WORKDIR /var/app


COPY requirements.txt .
COPY ./app .
# COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt