FROM python:3.9

WORKDIR /serialize_test

COPY requirements.txt /serialize_test

RUN pip install --upgrade pip -r requirements.txt

COPY . /serialize_test

EXPOSE 2000

CMD ["python", "serialize_test.py"]
