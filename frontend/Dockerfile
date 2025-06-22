FROM node:lts-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --force # Use npm ci for clean install, --force if needed for legacy deps

COPY . .
RUN npm run build -- --configuration=production