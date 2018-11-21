FROM python:3.6.7-stretch

# ENV DEBIAN_FRONTEND noninteractive
# ENV DEBIAN_FRONTEND teletype
# ENV PYTHONUNBUFFERED 1
ENV ORACLE_HOME /opt/oracle/instantclient_18_3
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:$ORACLE_HOME
ENV PATH $ORACLE_HOME:$PATH

RUN groupadd -r django \
    && useradd -r -g django django

RUN apt-get update -y && apt-get install -y --no-install-recommends apt-utils
RUN apt-get update -y && apt-get install apt-transport-https -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list | tee /etc/apt/sources.list.d/mssql-tools.list
RUN apt-get update -y && apt-get install unixodbc unixodbc-dev -y
RUN ACCEPT_EULA=Y apt-get install mssql-tools=14.0.6.0-1 -y
RUN apt-get install libaio1 libaio-dev -y
RUN apt-get install unzip -y
RUN apt-get install openssl

RUN mkdir -p /opt/oracle
COPY ./docker/production/django/instantclient-basic-linux.x64-18.3.0.0.0dbru.zip /opt/oracle/instantclient-basic-linux.x64-18.3.0.0.0dbru.zip
RUN unzip /opt/oracle/instantclient-basic-linux.x64-18.3.0.0.0dbru.zip -d /opt/oracle
# RUN ln -s /opt/oracle/instantclient_18_3/libclntsh.so.18.1 /opt/oracle/instantclient_18_3/libclntsh.so
# RUN ln -s /opt/oracle/instantclient_18_3/libocci.so.18.1 /opt/oracle/instantclient_18_3/libocci.so
# run  cd /opt/oracle/instantclient_12_2


# Install pre-requirement of PIP
RUN pip install --upgrade pip
RUN pip install --upgrade wheel

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./docker/local/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./docker/local/django/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

COPY ./docker/local/django/celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r//' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh

COPY ./docker/local/django/celery/beat/start.sh /start-celerybeat.sh
RUN sed -i 's/\r//' /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh

COPY ./docker/local/django/celery/flower/start.sh /start-flower.sh
RUN sed -i 's/\r//' /start-flower.sh
RUN chmod +x /start-flower.sh

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]