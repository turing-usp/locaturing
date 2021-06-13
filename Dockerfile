### Base image python foundation
FROM python:3.8
WORKDIR /locaturing

ARG TMDB_API_KEY
ENV TMDB_API_KEY=$TMDB_API_KEY

# Poetry installation (change later)
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /locaturing

CMD gunicorn app:server -b :8000 -t 30 --workers=1 --threads=1
