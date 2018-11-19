#!/usr/bin/env bash
# Utils functions
. ./../utils.sh

# Create envs vars if don't exist
ENV_FILES=(".env" "django/.env" "nginx/.env" "nginx/nginx.conf" "nginx/crons/renewssl.sh" "nginx/crons/crontab" "../../uwsgi.ini" "../../uwsgi.log" "postgres/.env" "mysql/.env" "sqlserver/.env" "mongo/.env" "couchdb/.env" "cassandra/.env" "neo4j/.env" "oracle/.env")
utils.check_envs_files "${ENV_FILES[@]}"

# Load environment vars, to use from console, run follow command:
# export $(cat envs | xargs)
utils.load_environment
utils.load_environment_django
utils.load_environment_nginx
utils.load_environment_permissions


# Menu options
if [[ "$1" == "machine.create" ]]; then
    utils.printer "Cheking if remote machine exist..."
    # If machine doesn't exist, create a droplet and provision machine
    if [[ "$MACHINE_DRIVER" == "do" ]]; then
        if [[ "$MACHINE_NAME" != $(docker-machine ls -q | grep "^$MACHINE_NAME$") ]]; then
            utils.printer "Starting machine if it's off..."
            docker-machine start $MACHINE_NAME
            utils.printer "Creating machine..."
            docker-machine create --driver digitalocean --digitalocean-access-token $DO_ACCESS_TOKEN --digitalocean-image $DO_IMAGE --digitalocean-size $DO_SIZE --digitalocean-region $DO_REGION $MACHINE_NAME
            utils.printer "Machine created at: $(docker-machine ip $MACHINE_NAME)"
        else
            utils.printer "Starting machine if it's off..."
            docker-machine start $MACHINE_NAME
            utils.printer "Machine already exist at: $(docker-machine ip $MACHINE_NAME)"
        fi
    elif [[ "$MACHINE_DRIVER" == "aws" ]]; then
        if [[ "$MACHINE_NAME" != $(docker-machine ls -q | grep "^$MACHINE_NAME$") ]]; then
            utils.printer "Creating machine..."
            docker-machine create --driver amazonec2 --amazonec2-access-key $AWS_ACCESS_KEY_ID --amazonec2-secret-key $AWS_SECRET_ACCESS_KEY --amazonec2-vpc-id $AWS_VPC_ID --amazonec2-region $AWS_DEFAULT_REGION --amazonec2-instance-type $AWS_INSTANCE_TYPE --amazonec2-root-size $AWS_ROOT_SIZE --amazonec2-ssh-user $AWS_SSH_USER $MACHINE_NAME
            utils.printer "Machine created at: $(docker-machine ip $MACHINE_NAME)"
        else
            utils.printer "Starting machine if it's off..."
            docker-machine start $MACHINE_NAME
            utils.printer "Machine already exist at: $(docker-machine ip $MACHINE_NAME)"
        fi
    elif [[ "$MACHINE_DRIVER" == "virtualbox" ]]; then
        if [[ "$MACHINE_NAME" != $(docker-machine ls -q | grep "^$MACHINE_NAME$") ]]; then
            utils.printer "Creating machine..."
            docker-machine create -d virtualbox $MACHINE_NAME
            utils.printer "Machine created at: $(docker-machine ip $MACHINE_NAME)"
        else
            utils.printer "Starting machine if it's off..."
            docker-machine start $MACHINE_NAME
            utils.printer "Machine already exist at: $(docker-machine ip $MACHINE_NAME)"
        fi
    elif [[ "$MACHINE_DRIVER" == "generic" ]]; then
        if [[ "$MACHINE_NAME" != $(docker-machine ls -q | grep "^$MACHINE_NAME$") ]]; then
            utils.printer "Machine doesn't exist."
        else
            utils.printer "Machine already exist at: $(docker-machine ip $MACHINE_NAME)"
        fi
    fi
elif [[ "$1" == "build.app" ]]; then
    utils.printer "Building services"
    docker-compose -f docker-compose.build.yaml build statics
    docker-compose -f docker-compose.build.yaml run statics
    docker-compose -f docker-compose.build.yaml build django
elif [[ "$1" == "build.nginx" ]]; then
    if [[ "$2" == "secure" ]]; then
        cp -R nginx/site.template.server.${ENVIRONMENT_MODE} nginx/site.template.ssl
        utils.printer "Setting default.conf based on site.template.ssl..."
        cp nginx/site.template.ssl nginx/default.conf
    else
        cp -R nginx/site.template.server.${ENVIRONMENT_MODE} nginx/site.template
        utils.printer "Setting default.conf based on site.template..."
        cp nginx/site.template nginx/default.conf
    fi
    utils.printer "Building images"
    docker-compose -f docker-compose.build.yaml build nginx
elif [[ "$1" == "build" ]]; then
    bash docker.sh build.app $2
    bash docker.sh build.nginx $2
elif [[ "$1" == "push" ]]; then
    utils.printer "Tagging images django..."
    utils.printer "${COMPOSE_PROJECT_NAME}_${SERVICE_DJANGO_BUILD_NAME} --> ${CONTAINER_REGISTRY_PREFIX}/${CONTAINER_REGISTRY_REPOSITORY_NAME}:${COMPOSE_PROJECT_NAME}-${SERVICE_DJANGO_BUILD_NAME}-${SERVICE_DJANGO_BUILD_TAG_CALC}"
    docker tag "${COMPOSE_PROJECT_NAME}_${SERVICE_DJANGO_BUILD_NAME}" "${CONTAINER_REGISTRY_PREFIX}/${CONTAINER_REGISTRY_REPOSITORY_NAME}:${COMPOSE_PROJECT_NAME}-${SERVICE_DJANGO_BUILD_NAME}-${SERVICE_DJANGO_BUILD_TAG_CALC}"
    utils.printer "Tagging images nginx..."
    utils.printer "${COMPOSE_PROJECT_NAME}_${SERVICE_NGINX_BUILD_NAME} --> ${CONTAINER_REGISTRY_PREFIX}/${CONTAINER_REGISTRY_REPOSITORY_NAME}:${COMPOSE_PROJECT_NAME}-${SERVICE_NGINX_BUILD_NAME}-${SERVICE_NGINX_BUILD_TAG_CALC}"
    docker tag "${COMPOSE_PROJECT_NAME}_${SERVICE_NGINX_BUILD_NAME}" "${CONTAINER_REGISTRY_PREFIX}/${CONTAINER_REGISTRY_REPOSITORY_NAME}:${COMPOSE_PROJECT_NAME}-${SERVICE_NGINX_BUILD_NAME}-${SERVICE_NGINX_BUILD_TAG_CALC}"
    if [[ "${CONTAINER_REGISTRY_SERVICE}" == "dockerhub" ]]; then
        utils.printer "Loggin in DockerHub"
        docker login -u ${CONTAINER_REGISTRY_USER} -p ${CONTAINER_REGISTRY_PASS}
    elif [[ "${CONTAINER_REGISTRY_SERVICE}" == "aws" ]]; then
        $(aws ecr get-login --no-include-email --region ${AWS_DEFAULT_REGION})
    fi
    utils.printer "Push images..."
    docker push "${CONTAINER_REGISTRY_PREFIX}/${CONTAINER_REGISTRY_REPOSITORY_NAME}:${COMPOSE_PROJECT_NAME}-${SERVICE_DJANGO_BUILD_NAME}-${SERVICE_DJANGO_BUILD_TAG_CALC}"
    docker push "${CONTAINER_REGISTRY_PREFIX}/${CONTAINER_REGISTRY_REPOSITORY_NAME}:${COMPOSE_PROJECT_NAME}-${SERVICE_NGINX_BUILD_NAME}-${SERVICE_NGINX_BUILD_TAG_CALC}"
elif [[ "$1" == "deploy" ]]; then
    utils.printer "Pulling images"
    docker-compose $(docker-machine config $MACHINE_NAME) pull
    utils.printer "Deploying services"
    docker-compose $(docker-machine config $MACHINE_NAME) up -d django postgres redis celeryworker celerybeat flower
    utils.printer "Your application is deployed in: $(docker-machine ip $MACHINE_NAME)"
elif [[ "$1" == "server.renewssl.cerbot" ]]; then
    if [[ "$2" == "secure" ]]; then
        utils.printer "Stopping nginx machine if it's running..."
        docker-compose $(docker-machine config $MACHINE_NAME) stop nginx
        utils.printer "Creating letsencrypt certifications files..."
        docker-compose $(docker-machine config $MACHINE_NAME) up certbot
    fi
elif [[ "$1" == "server.renewssl.cronjob" ]]; then
    if [[ "$2" == "secure" ]]; then
        utils.printer "Set nginx service renewssl vars..."
        utils.nginx_renewssl_vars
        utils.printer "Setting up cron job for auto renew ssl..."
        CRONPATHTMP=/home/ubuntu/${COMPOSE_PROJECT_NAME}
        CRONTPAHTFINAL=/opt/crons/${COMPOSE_PROJECT_NAME}
        docker-machine ssh $MACHINE_NAME sudo mkdir -p $CRONPATHTMP
        docker-machine ssh $MACHINE_NAME sudo mkdir -p $CRONTPAHTFINAL
        docker-machine ssh $MACHINE_NAME sudo chown -R ubuntu:ubuntu $CRONPATHTMP
        docker-machine scp -r nginx/crons $MACHINE_NAME:$CRONPATHTMP
        docker-machine ssh $MACHINE_NAME sudo cp -r $CRONPATHTMP/* $CRONTPAHTFINAL
        docker-machine ssh $MACHINE_NAME sudo chmod +x $CRONTPAHTFINAL/crons/renewssl.sh
        docker-machine ssh $MACHINE_NAME sudo touch $CRONTPAHTFINAL/crons/renewssl.logs
        docker-machine ssh $MACHINE_NAME sudo crontab $CRONTPAHTFINAL/crons/crontab
    fi
elif [[ "$1" == "server.deploy" ]]; then
    utils.printer "Deploying nginx machine service"
    docker-compose $(docker-machine config $MACHINE_NAME) up -d nginx
elif [[ "$1" == "server.up" ]]; then
    bash docker.machine.sh server.renewssl.cerbot $2
    bash docker.machine.sh server.deploy $2
    bash docker.machine.sh server.renewssl.cronjob $2
elif [[ "$1" == "up" ]]; then
    # Create machine
    bash docker.machine.sh machine.create
    # Build meteor && docker images
    bash docker.machine.sh build $2
    # Pushing images to docker hub
    bash docker.machine.sh push
    # Deploying services to remote machine server
    bash docker.machine.sh deploy
    # Set server configuration
    bash docker.machine.sh server.up $2
elif [[ "$1" == "start" ]]; then
    utils.printer "Start services"
    docker-compose $(docker-machine config $MACHINE_NAME) start $2
elif [[ "$1" == "restart" ]]; then
    utils.printer "Restart services"
    docker-compose $(docker-machine config $MACHINE_NAME) restart $2
elif [[ "$1" == "stop" ]]; then
    utils.printer "Stop services"
    docker-compose $(docker-machine config $MACHINE_NAME) stop $2
elif [[ "$1" == "rm" ]]; then
    utils.printer "Stop && remove services"
    docker-compose $(docker-machine config $MACHINE_NAME) stop $2
    docker-compose $(docker-machine config $MACHINE_NAME) rm $2
elif [[ "$1" == "bash" ]]; then
    if [[ ! -z "$2" ]]; then
        utils.printer "Connect to $2 bash shell"
        docker-compose $(docker-machine config $MACHINE_NAME) exec $2 bash
    else
        utils.printer "You should specify the service name: django | postgres | redis | nginx | certbot | celeryworker | celerybeat | flower | bower | pgadmin"
    fi
elif [[ "$1" == "sh" ]]; then
    if [[ ! -z "$2" ]]; then
        utils.printer "Connect to $2 bash shell"
        docker-compose $(docker-machine config $MACHINE_NAME) exec $2 sh
    else
        utils.printer "You should specify the service name: django | postgres | redis | nginx | certbot | celeryworker | celerybeat | flower | bower | pgadmin"
    fi
elif [[ "$1" == "logs" ]]; then
    if [[ ! -z "$2" ]]; then
        utils.printer "Showing logs..."
        if [[ -z "$3" ]]; then
            docker-compose $(docker-machine config $MACHINE_NAME) logs -f $2
        else
            docker-compose $(docker-machine config $MACHINE_NAME) logs -f --tail=$3 $2
        fi
    else
        utils.printer "You should specify the service name: django | postgres | redis | nginx | certbot | celeryworker | celerybeat | flower | bower | pgadmin"
    fi
elif [[ "$1" == "ps" ]]; then
    utils.printer "Show all running containers"
    docker-compose $(docker-machine config $MACHINE_NAME) ps
elif [[ "$1" == "machine.details" ]]; then
    utils.printer "Searching for machine details..."
    if [[ "$MACHINE_NAME" != $(docker-machine ls -q | grep "^$MACHINE_NAME$") ]]; then
        utils.printer "Machine doesn't exist"
    else
        utils.printer "Machine driver: $MACHINE_DRIVER"
        utils.printer "Machine name: $MACHINE_NAME"
        utils.printer "Machine ip: $(docker-machine ip $MACHINE_NAME)"
    fi
elif [[ "$1" == "machine.start" ]]; then
    if [[ "$MACHINE_NAME" != $(docker-machine ls -q | grep "^$MACHINE_NAME$") ]]; then
        utils.printer "Machine doesn't exist"
    else
        utils.printer "Power on machine..."
        docker-machine rm $MACHINE_NAME
    fi
elif [[ "$1" == "machine.restart" ]]; then
    if [[ "$MACHINE_NAME" != $(docker-machine ls -q | grep "^$MACHINE_NAME$") ]]; then
        utils.printer "Machine doesn't exist"
    else
        utils.printer "Restarting on machine..."
        docker-machine restart $MACHINE_NAME
    fi
elif [[ "$1" == "machine.stop" ]]; then
    if [[ "$MACHINE_NAME" != $(docker-machine ls -q | grep "^$MACHINE_NAME$") ]]; then
        utils.printer "Machine doesn't exist"
    else
        utils.printer "Power off machine..."
        docker-machine stop $MACHINE_NAME
    fi
elif [[ "$1" == "machine.rm" ]]; then
    if [[ "$MACHINE_NAME" != $(docker-machine ls -q | grep "^$MACHINE_NAME$") ]]; then
        utils.printer "Machine doesn't exist"
    else
        utils.printer "Power off machine..."
        docker-machine stop $MACHINE_NAME
        utils.printer "Removing machine..."
        docker-machine rm $MACHINE_NAME
    fi
elif [[ "$1" == "machine.ssh" ]]; then
    if [[ "$MACHINE_NAME" != $(docker-machine ls -q | grep "^$MACHINE_NAME$") ]]; then
        utils.printer "Machine doesn't exist"
    else
        utils.printer "Conecting via ssh to \"$MACHINE_NAME\" machine..."
        docker-machine ssh $MACHINE_NAME
    fi
else
    utils.printer "Params between {} are optional, except {}*"
    utils.printer "Service names: django | postgres | redis | nginx | certbot | celeryworker | celerybeat | flower | bower | pgadmin"
    utils.printer ""
    utils.printer "Usage: docker.machine.sh [build|deploy|server.up|up|start|restart|stop|rm|sh|bash|logs|machine.[details|create|start|restart|stop|rm|ssh]]"
    echo -e "build {secure}                  --> Build services; \"secure\" parameter is optional for ssl configuration"
    echo -e "deploy                          --> Build and run services"
    echo -e "server.up {secure}              --> Build and run server (nginx) services; \"secure\" parameter is optional for ssl configuration"
    echo -e "up {secure}                     --> Build && deploy services; \"secure\" parameter is optional for ssl configuration"
    echo -e "start {service}                 --> Start services"
    echo -e "restart {service}               --> Restart services"
    echo -e "stop {service}                  --> Stop services"
    echo -e "rm {service}                    --> Stop && remove services"
    echo -e "sh {service}*                   --> Connect to \"service\" shell"
    echo -e "bash {service}*                 --> Connect to \"service\" bash shell"
    echo -e "logs {service}* {n_last_lines}  --> Show \"service\" server logs"
    echo -e "ps                              --> Show all running containers"
    echo -e "machine.[details|create|start|restart|stop|rm|ip|ssh] --> Machine actions"
fi
