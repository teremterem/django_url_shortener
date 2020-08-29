FROM python:3

ENV PYTHONUNBUFFERED 1
# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
# https://github.com/awslabs/amazon-sagemaker-examples/issues/319

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
