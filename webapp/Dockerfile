# build environment
FROM node:13.12.0-alpine as build
ARG CONFIG_FILE=""
ENV CONFIG_FILE=$CONFIG_FILE
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json ./
COPY package-lock.json ./
RUN npm ci --silent
RUN npm install react-scripts@3.4.1 -g --silent
COPY . ./
RUN echo $CONFIG_FILE
RUN echo $CONFIG_FILE | base64 -d > src/config/engine.json
RUN cat src/config/engine.json
RUN npm run build

# production environment
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
