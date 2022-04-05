FROM python:3.10-alpine

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./pyredditlive.py .

CMD ["python3", "pyredditlive.py"]