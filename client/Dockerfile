# ----------------------------------------------------------------------
# Build Stage
# ----------------------------------------------------------------------
FROM node:22-slim AS build

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy project code and build the project.
COPY . .
RUN npm run build

# ----------------------------------------------------------------------
# Production Stage
# ----------------------------------------------------------------------
FROM nginx

# Copy the application from the build stage.
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the nginx configuration.
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

