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


# Install uWSGI
RUN apt-get install python-mysqldb
RUN pip3 install uwsgi

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --no-cache-dir -r /requirements/production.txt

RUN pip install --no-cache-dir -r /requirements/extra.txt \
    && rm -rf /requirements

RUN cp /etc/odbcinst.ini /etc/odbc.ini
RUN ln -s /etc/odbc.ini /usr/local/etc/odbc.ini

COPY ./docker/production/django/uwsgi.sh /uwsgi.sh
RUN sed -i 's/\r//' /uwsgi.sh
RUN chmod +x /uwsgi.sh
# RUN chown django /uwsgi.sh

COPY ./docker/production/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh
RUN chmod +x /entrypoint.sh
# RUN chown django /entrypoint.sh

COPY ./docker/production/django/celery/worker/start.sh /start-celeryworker.sh
RUN sed -i 's/\r//' /start-celeryworker.sh
RUN chmod +x /start-celeryworker.sh
# RUN chown django /start-celeryworker.sh

COPY ./docker/production/django/celery/beat/start.sh /start-celerybeat.sh
RUN sed -i 's/\r//' /start-celerybeat.sh
RUN chmod +x /start-celerybeat.sh
# RUN chown django /start-celerybeat.sh

COPY ./docker/production/django/celery/flower/start.sh /start-flower.sh
RUN sed -i 's/\r//' /start-flower.sh
RUN chmod +x /start-flower.sh
# RUN chown django /start-flower.sh

COPY . /app

# RUN chown django /opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.2.so.0.1
# RUN chown -R django /app

# USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]