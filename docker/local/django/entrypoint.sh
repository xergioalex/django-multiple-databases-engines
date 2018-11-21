#!/usr/bin/env bash

# basset -o errexit
# set -o pipefail

# todo: turn on after #1295
# set -o nounset


# This entrypoint is used to play nicely with the current cookiecutter configuration.
# Since docker-compose relies heavily on environment variables itself for configuration, we'd have to define multiple
# environment variables just to support cookiecutter out of the box. That makes no sense, so this little entrypoint
# does all this for us.
export REDIS_URL=redis://redis:6379

# the official postgres image uses 'postgres' as default user if not set explictly.
if [ -z "${POSTGRES_USER}" ]; then
    base_postgres_image_default_user='postgres'
    export POSTGRES_USER="${base_postgres_image_default_user}"
fi

export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

export CELERY_BROKER_URL="${REDIS_URL}"


postgres_ready() {
python << END
import sys
import psycopg2

try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}",
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

exec "$@"



echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"
echo -e "${GREEN}                                          [Datalab Utils]                                       ${NC}"
echo -e "${ORANG}                                 This scripts installs MSSQL drivers                            ${NC}"
echo -e "${ORANG}                                  E. Marinetto (nenetto@gmail.com)                               ${NC}"
echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"

echo -e "${GREEN}[Datalab Utils] ${ORANG}Creating log${NC}"
DIRECTORY=$(cd `dirname $0` && pwd)
LOGFILE=$DIRECTORY'/installation.log'

echo -e "${GREEN}[Datalab Utils] ${ORANG}Updating sources${NC}"
apt-get update >> $LOGFILE 2>$LOGFILE && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends apt-utils >> $LOGFILE 2>$LOGFILE


echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing apt-transport-https${NC}"
DEBIAN_FRONTEND=noninteractive apt-get -y install apt-transport-https curl >> $LOGFILE

echo -e "${GREEN}[Datalab Utils] ${ORANG}Adding key${NC}"
curl https://packages.microsoft.com/keys/microsoft.asc 2>$LOGFILE | apt-key add - >> $LOGFILE 2>$LOGFILE

#Download appropriate package for the OS version
#Choose only ONE of the following, corresponding to your OS version

#Debian 8
echo -e "${GREEN}[Datalab Utils] ${ORANG}Adding sources${NC}"
curl https://packages.microsoft.com/config/debian/8/prod.list > /etc/apt/sources.list.d/mssql-release.list 2>$LOGFILE

#Debian 9
#curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list

echo -e "${GREEN}[Datalab Utils] ${ORANG}Updating sources${NC}"
apt-get update >> $LOGFILE
echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing msodbcsql13${NC}"
DEBIAN_FRONTEND=noninteractive ACCEPT_EULA=Y apt-get -y install msodbcsql >> $LOGFILE

# optional: for bcp and sqlcmd
echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing mssql-tools13${NC}"
DEBIAN_FRONTEND=noninteractive ACCEPT_EULA=Y apt-get -y install mssql-tools >> $LOGFILE

# optional: for unixODBC development headers
echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing  unixodbc-dev${NC}"
DEBIAN_FRONTEND=noninteractive apt-get install -y unixodbc-dev >> $LOGFILE

echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing  libssl1.0.0${NC}"
echo "deb http://security.debian.org/debian-security jessie/updates main" >> /etc/apt/sources.list
apt-get update >> $LOGFILE
DEBIAN_FRONTEND=noninteractive apt-get install libssl1.0.0 >>$LOGFILE

echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing  python-pyodbc${NC}"
DEBIAN_FRONTEND=noninteractive apt-get -y install python-pyodbc >> $LOGFILE

echo -e "${GREEN}[Datalab Utils] ${ORANG}Installing  locales${NC}"
DEBIAN_FRONTEND=noninteractive apt-get -y install locales >> $LOGFILE
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
locale-gen >> $LOGFILE

echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"
echo -e "${GREEN}                                        [Datalab Utils]                                         ${NC}"
echo -e "${GREEN}                                          FINISHED :D                                           ${NC}"
echo -e "${BLUEE}------------------------------------------------------------------------------------------------${NC}"


exec "$@"
