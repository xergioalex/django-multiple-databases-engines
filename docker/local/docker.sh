#!/usr/bin/env bash

# Utils functions
. ./../utils.sh

# Create envs vars if don't exist
ENV_FILES=(".env" "django/.env" "postgres/.env" "mysql/.env" "sqlserver/.env" "oracle/.env" "mongo/.env" "couchdb/.env")
utils.check_envs_files "${ENV_FILES[@]}"

# Load environment vars, to use from console, run follow command:
utils.load_environment
utils.load_environment_permissions

# Menu options
if [[ "$1" == "build" ]]; then
    utils.printer "Building images"
    docker-compose build $2
elif [[ "$1" == "up" ]]; then
    if [[ ! -z "$2" ]]; then
        utils.printer "Building images"
        docker-compose build $2
        utils.printer "Starting services"
        docker-compose up -d $2
    else
        utils.printer "Building images"
        docker-compose build
        utils.printer "Starting services"
        docker-compose up -d django postgres redis celeryworker celerybeat flower
    fi
elif [[ "$1" == "up.pgadmin" ]]; then
    utils.printer "Run pgadmin service"
    docker-compose -f docker-compose.pgadmin.yaml up -d
elif [[ "$1" == "start" ]]; then
    utils.printer "Start services"
    docker-compose start $2
elif [[ "$1" == "restart" ]]; then
    utils.printer "Restart services"
    docker-compose restart $2
elif [[ "$1" == "stop" ]]; then
    utils.printer "Stop services"
    docker-compose stop $2
elif [[ "$1" == "rm" ]]; then
    utils.printer "Remove services"
    docker-compose rm $2
elif [[ "$1" == "ps" ]]; then
    utils.printer "Show all running containers"
    docker-compose ps $2
elif [[ "$1" == "bash" ]]; then
    if [[ ! -z "$2" ]]; then
        utils.printer "Connect to $2 bash shell"
        docker-compose exec $2 bash
    else
        utils.printer "You should specify the service name: django | postgres | celeryworker | redis | celerybeat | flower | pgadmin"
    fi
elif [[ "$1" == "sh" ]]; then
    if [[ ! -z "$2" ]]; then
        utils.printer "Connect to $2 sh shell"
        docker-compose exec $2 sh
    else
        utils.printer "You should specify the service name: django | postgres | celeryworker | redis | celerybeat | flower | pgadmin"
    fi
elif [[ "$1" == "logs" ]]; then
    if [[ ! -z "$2" ]]; then
        utils.printer "Showing logs..."
        if [[ -z "$3" ]]; then
            docker-compose logs -f $2
        else
            docker-compose logs -f --tail=$3 $2
        fi
    else
        utils.printer "You should specify the service name: django | postgres | celeryworker | redis | celerybeat | flower | pgadmin"
    fi
else
    utils.printer "Service names: django | postgres | celeryworker | redis | celerybeat | flower | pgadmin"
    utils.printer "Params between {} are optional"
    utils.printer "Usage: docker.sh [build|up|start|restart|stop|rm|sh|bash|logs|ps]"
    echo -e "build {service} --> Build services"
    echo -e "up {service} --> Run services"
    echo -e "start {service} --> Start services"
    echo -e "restart {service} --> Restart services"
    echo -e "stop {service} --> Stop services"
    echo -e "rm {service} --> Remove services"
    echo -e "sh service --> Connect to \"service\" service shell"
    echo -e "bash service --> Connect to \"service\" service bash shell"
    echo -e "logs {n_last_lines} --> Show \"service\" server logs"
    echo -e "help --> Show menu options"
fi
