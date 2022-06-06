FROM python:3.9
RUN apt-get update && apt-get install -y \
     #default-libmysqlclient-dev \
     libpq-dev \
     automake \
     build-essential \
     && rm -rf /var/lib/apt/lists/*
EXPOSE 8080
WORKDIR /app 
COPY requirements.txt /app
RUN pip3 install setuptools
RUN pip3 install wheel
RUN pip3 install buildtools
RUN pip3 install -r requirements.txt --no-cache-dir
#COPY . /app 
#RUN ["python3", "manage.py", "collectstatic", "--noinput"]
ENTRYPOINT ["uwsgi", "--ini", "uwsgi.ini"]