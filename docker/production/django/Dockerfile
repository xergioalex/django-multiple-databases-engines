FROM python:3.6.7-stretch

# ENV DEBIAN_FRONTEND noninteractive
# ENV DEBIAN_FRONTEND teletype
# ENV PYTHONUNBUFFERED 1

RUN groupadd -r django \
    && useradd -r -g django django

RUN apt-get update -y && apt-get install -y --no-install-recommends apt-utils
RUN apt-get update -y && apt-get install apt-transport-https -y
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list | tee /etc/apt/sources.list.d/mssql-tools.list
RUN apt-get update -y && apt-get install unixodbc unixodbc-dev -y
RUN ACCEPT_EULA=Y apt-get install mssql-tools=14.0.6.0-1 -y
RUN apt-get install libaio1 libaio-dev -y
# RUN apt-get remove msodbcsql
# RUN apt-cache madison msodbcsql
# RUN apt-get install msodbcsql=13.1.9.2-1 -y
# RUN apt-cache madison mssql-tools
# RUN ACCEPT_EULA=Y apt-get install mssql-tools=14.0.6.0-1 -y
# RUN apt-mark hold mssql-tools
# RUN apt-mark hold msodbcsql


# Install uWSGI
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