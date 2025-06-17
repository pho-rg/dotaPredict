# build step
FROM node:20 AS builder

WORKDIR /app

COPY package*.json ./
COPY vite.config.* ./
COPY . .

RUN npm install
RUN npm run build

# hosting step
FROM nginx:alpine

# copying the built app
COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
