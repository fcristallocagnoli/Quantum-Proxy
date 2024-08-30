# ----------------------------
# build from source
# ----------------------------
FROM node:lts-alpine AS build

WORKDIR /app

# 'develop' como build predeterminada
ARG BUILD_MODE=develop

COPY package*.json .
RUN npm ci

COPY . .
RUN npm run ${BUILD_MODE}

# ----------------------------
# develop/docker mode
# ----------------------------
FROM build as develop

RUN npm install -g @angular/cli@17

EXPOSE 4200

CMD [ "ng", "serve", "--host", "0.0.0.0" ]

# ----------------------------
# run with nginx
# ----------------------------
FROM nginx:latest as product

COPY nginx.conf /etc/nginx/conf.d
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html

EXPOSE 80

CMD [ "nginx", "-g", "daemon off;" ]