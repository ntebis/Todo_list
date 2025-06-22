# Stage 1: Build the Angular application
FROM node:20-alpine as build

WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package*.json ./

# Install dependencies
RUN npm install

RUN npm install -g @angular/cli

# Copy the rest of the application files
COPY . .

# Build the Angular application (development mode)
# Using --configuration=development ensures development-specific settings are applied
# --watch is NOT used here as it's better handled by the development server in the next stage
# RUN npm run build --configuration=development

# # Stage 2: Serve the Angular application with a development server
# FROM node:20-alpine

# WORKDIR /app

# # Copy built Angular application from the build stage
# COPY --from=build /app/dist/todo-frontend ./dist

# # Copy package.json and node_modules for running the dev server and other npm scripts
# # We only copy what's absolutely necessary to keep the final image smaller
# COPY package*.json ./
# COPY --from=build /app/node_modules ./node_modules

# # Expose the port Angular CLI development server typically runs on
# EXPOSE 4200


# CMD ["npm", "start", "--", "--host", "0.0.0.0", "--port", "80"]
ENTRYPOINT ["./entrypoint.sh"]
# CMD ["ng", "serve", "--host", "0.0.0.0"]