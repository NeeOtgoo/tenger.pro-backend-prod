FROM  python:3.10.6

ENV PYTHONUNBUFFERED=1

WORKDIR /server

RUN pip install django django-cors-headers

# copy from the current directory of the Dockerfile to /api in the image
COPY . . 

EXPOSE 8100
