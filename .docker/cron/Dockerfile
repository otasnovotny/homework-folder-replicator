FROM python:3.12.1

# reducing the size of Docker image and preventing unnecessary files from being created during the build process.
ENV PYTHONDONTWRITEBYTECODE=1

# outputs data immediately rather than buffering it
ENV PYTHONUNBUFFERED=1

RUN apt-get -y update
RUN apt-get -y install cron vim

WORKDIR /app
#COPY ./requirements.txt ./requirements.txt

RUN pip3 install --upgrade pip
#RUN pip3 install -r requirements.txt

COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

CMD ["cron", "-f"]
