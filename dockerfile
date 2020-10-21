FROM python:3.8

RUN mkdir -p /opt/services/djangoapp/src
WORKDIR /opt/services/djangoapp/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install and enable ssh service
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
        && apt-get install -y --no-install-recommends dialog \
        && apt-get update \
  && apt-get install -y --no-install-recommends openssh-server \
  && echo "$SSH_PASSWD" | chpasswd
COPY ./sshd_config /etc/ssh/

# install dependencies
RUN python -m pip install --upgrade pip setuptools wheel


COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir media
RUN mkdir media/travel
RUN mkdir media/travel/temp
RUN mkdir media/inventory
RUN mkdir media/inventory/temp

COPY . /opt/services/djangoapp/src

EXPOSE 80 8000 2222

COPY ./azure_scripts/init.sh /usr/local/bin/
	
RUN chmod u+x /usr/local/bin/init.sh
ENTRYPOINT ["init.sh"]
