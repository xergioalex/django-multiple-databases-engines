#!/bin/bash

# ----------- UTILS FUNCTIONS -----------

# Printer with shell colors
function utils.printer {
    # BASH COLORS
    GREEN='\033[0;32m'
    RESET='\033[0m'
    echo -e "${GREEN}$(date +"%b %d %r") - $1${RESET}"
}

# Check container status and PORT status
function utils.checkContainerPortStatus {
    if [[ ! -z $1 ]] && [[ ! -z $2 ]]; then
        while [[ $(docker inspect --format='{{.State.Status}}' $1) == "running" ]] || [[ ! -z "$(lsof -i :$2)" ]]; do
            utils.printer "Waiting for \"$1\" stop and free \"$2\" PORT"
            sleep 1
        done
    fi
}


# ------------ MAIN SCRIPT ---------------

# Docker container service names
NGINX_SERVICE_CONTAINER=
CERTBOT_SERVICE_CONTAINER=

utils.printer "-------------------------------------------------------------------------------"
utils.printer "Renew Certificate Job"
utils.printer "-------------------------------------------------------------------------------"

utils.printer "Step 0: Check configuration vars"
if [[ ! -z $NGINX_SERVICE_CONTAINER ]] && [[ ! -z $CERTBOT_SERVICE_CONTAINER ]]; then
    utils.printer "Step 1: Stop nginx service"
    docker stop $NGINX_SERVICE_CONTAINER
    utils.checkContainerPortStatus $NGINX_SERVICE_CONTAINER 80

    utils.printer "Step 2: Create or renew certificates"
    utils.printer "Start cerbot service"
    docker restart $CERTBOT_SERVICE_CONTAINER
    utils.checkContainerPortStatus $CERTBOT_SERVICE_CONTAINER 80

    utils.printer "Step 3: Restart nginx service"
    docker restart $NGINX_SERVICE_CONTAINER
else
    utils.printer "Something is wrong, one ore more configuration vars are empty"
fi
