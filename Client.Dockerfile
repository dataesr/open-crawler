FROM node:18-alpine
WORKDIR /app
COPY ./client/package*.json ./
RUN npm ci --silent
COPY ./client .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
