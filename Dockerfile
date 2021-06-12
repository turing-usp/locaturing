### Base image python foundation

FROM python:3.8

# RUN apk add --no-cache gcc python3-dev musl-dev libffi-dev openssl-dev jpeg-dev zlib-dev build-base make tiff-dev poppler-utils
# RUN apk add --no-cache openssh git

# Poetry installation (change later)
RUN pip install poetry
RUN poetry install

COPY . /locaturing
WORKDIR /locaturing

CMD gunicorn app:server -b :8000 -t 10 --workers=2 --threads=1