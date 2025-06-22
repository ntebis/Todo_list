#!/bin/sh

# workaround because i could make nginx to work
# cp /app/src/app/assets/env.template.js /app/src/app/assets/env.js
rm /app/src/app/environments/environment.ts
cp /app/src/app/environments/environment-container.ts /app/src/app/environments/environment.ts
exec npm start -- --host 0.0.0.0 --port 80