#!/usr/bin/env bash

# Printer with shell colors
function utils.printer {
	# BASH COLORS
	GREEN='\033[0;32m'
    RESET='\033[0m'
	if [[ ! -z "$2" ]]; then
		# print new line before
    	echo ""
    fi
    echo -e "${GREEN}$1${RESET}"
}


# Create enviroment files if don't exists
function utils.check_envs_files {
	ENV_FILES=("$@")
	for i in "${ENV_FILES[@]}";  do
		if [[ ! -f "$i" ]]; then
			cp "$i.example" "$i"
		fi
	done
}

# Load environment vars in root directory
function utils.uppercase {
	echo $1 | awk '{print toupper($0)}'
}

# Load environment vars in root directory
function utils.current_folder_name {
	echo $(pwd | grep -o '[^/]*$') | tr "[:upper:]" "[:lower:]"
}

# Load environment vars in root directory
function utils.load_environment {
	if [[ ! -z $(cat .env | xargs)  ]]; then
	    # export $(grep -vwE "#" .env | xargs)
	    set -a
		source .env
		set +a
	fi
}

# Load environment vars in root directory
function utils.load_environment_permissions {
	PERMISSIONS="$(id -u):$(id -g)"
	sed -i.bak "s/.*SERVICE_PERMISSIONS.*/SERVICE_PERMISSIONS=$PERMISSIONS/" .env
	rm  .env.bak
}


# Load settings var enviroment
function utils.load_environment_django {
	# Set build tag
	export SERVICE_DJANGO_BUILD_TAG_CALC=${SERVICE_DJANGO_BUILD_TAG}-latest
	if [[ ! -z "${BUILD_NUMBER}" ]]; then
		sed -i /SERVICE_DJANGO_BUILD_NUMBER/c\SERVICE_DJANGO_BUILD_NUMBER=${BUILD_NUMBER} .env
		export BUILD_DJANGO_NUMBER_CALC=${BUILD_NUMBER}
		if [[ ! -z "${SERVICE_DJANGO_BUILD_AMOUNT}" ]]; then
			export BUILD_DJANGO_NUMBER_CALC=$((${BUILD_NUMBER}%${SERVICE_DJANGO_BUILD_AMOUNT}))
	    fi
	    export SERVICE_DJANGO_BUILD_TAG_CALC=${SERVICE_DJANGO_BUILD_TAG}-${BUILD_DJANGO_NUMBER_CALC}
	else [[ ! -z "${SERVICE_DJANGO_BUILD_NUMBER}" ]]
		export BUILD_DJANGO_NUMBER_CALC=${SERVICE_DJANGO_BUILD_NUMBER}
		if [[ ! -z "${SERVICE_DJANGO_BUILD_AMOUNT}" ]]; then
			export BUILD_DJANGO_NUMBER_CALC=$((${SERVICE_DJANGO_BUILD_NUMBER}%${SERVICE_DJANGO_BUILD_AMOUNT}))
	    fi
	    export SERVICE_DJANGO_BUILD_TAG_CALC=${SERVICE_DJANGO_BUILD_TAG}-${BUILD_DJANGO_NUMBER_CALC}
	fi
}

# Set nginx service renewssl vars...
function utils.nginx_renewssl_vars {
	# Setup container service names
	sed -i /NGINX_SERVICE_CONTAINER=/c\NGINX_SERVICE_CONTAINER=${COMPOSE_PROJECT_NAME}_nginx_1 nginx/crons/renewssl.sh
    sed -i /CERTBOT_SERVICE_CONTAINER=/c\CERTBOT_SERVICE_CONTAINER=${COMPOSE_PROJECT_NAME}_certbot_1 nginx/crons/renewssl.sh

    # Setup cron job vars
    cp nginx/crons/crontab.example nginx/crons/crontab
    sed -i -e "s/COMPOSE_PROJECT_NAME/$COMPOSE_PROJECT_NAME/g" nginx/crons/crontab
}

# Load settings var enviroment
function utils.load_environment_nginx {
	# Set build tag
	export SERVICE_NGINX_BUILD_TAG_CALC=${SERVICE_NGINX_BUILD_TAG}-latest
	if [[ ! -z "${BUILD_NUMBER}" ]]; then
		sed -i /SERVICE_NGINX_BUILD_NUMBER/c\SERVICE_NGINX_BUILD_NUMBER=${BUILD_NUMBER} .env
		export BUILD_NGINX_NUMBER_CALC=${BUILD_NUMBER}
		if [[ ! -z "${SERVICE_NGINX_BUILD_AMOUNT}" ]]; then
			export BUILD_NGINX_NUMBER_CALC=$((${BUILD_NUMBER}%${SERVICE_NGINX_BUILD_AMOUNT}))
	    fi
	    export SERVICE_NGINX_BUILD_TAG_CALC=${SERVICE_NGINX_BUILD_TAG}-${BUILD_NGINX_NUMBER_CALC}
	else [[ ! -z "${SERVICE_NGINX_BUILD_NUMBER}" ]]
		export BUILD_NGINX_NUMBER_CALC=${SERVICE_NGINX_BUILD_NUMBER}
		if [[ ! -z "${SERVICE_NGINX_BUILD_AMOUNT}" ]]; then
			export BUILD_NGINX_NUMBER_CALC=$((${SERVICE_NGINX_BUILD_NUMBER}%${SERVICE_NGINX_BUILD_AMOUNT}))
	    fi
	    export SERVICE_NGINX_BUILD_TAG_CALC=${SERVICE_NGINX_BUILD_TAG}-${BUILD_NGINX_NUMBER_CALC}
	fi
}