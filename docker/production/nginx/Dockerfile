FROM nginx:1.13.8-alpine

MAINTAINER xergioalex@gmail.com

# Create logs files
RUN mkdir -p /etc/nginx/logs && \
	touch /etc/nginx/logs/site.access && \
	touch /etc/nginx/logs/site.error

# Copy custom configuration files
COPY docker/production/nginx/nginx.conf /etc/nginx/nginx.conf
COPY docker/production/nginx/default.conf /etc/nginx/conf.d/default.conf

# Copy Staticfiles of Django
# COPY ./staticfiles /opt/staticfiles

# Run nginx
CMD nginx -g 'daemon off;'
