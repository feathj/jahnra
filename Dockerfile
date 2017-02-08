FROM python:2.7

RUN mkdir /app
COPY requirements.txt /app

WORKDIR /app
RUN pip install -r requirements.txt

# Download nltk db
RUN python -m nltk.downloader -d /usr/local/share/nltk_data stopwords
