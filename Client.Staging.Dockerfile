FROM node:18-alpine AS build
WORKDIR /app
COPY ./client/package*.json ./
RUN npm ci --silent
COPY ./client .
RUN npm run build

# production environment
FROM nginx:stable
COPY --from=build /app/dist /usr/share/nginx/html
COPY .client/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
