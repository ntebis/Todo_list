#!/bin/sh


envsubst < /usr/share/nginx/html/assets/env.template.js > /usr/share/nginx/html/assets/env.js

# Start Nginx (or your web server)
exec nginx -g 'daemon off;'