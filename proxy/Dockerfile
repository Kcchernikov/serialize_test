FROM python:3.9

WORKDIR /proxy

COPY requirements.txt /proxy

RUN pip install --upgrade pip -r requirements.txt

COPY . /proxy

EXPOSE 2000

CMD ["python", "proxy.py"]
