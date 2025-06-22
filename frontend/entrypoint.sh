#!/bin/sh


envsubst < src/app/html/assets/env.template.js > src/app/html/assets/env.js

# Start Nginx (or your web server)
exec nginx -g 'daemon off;'