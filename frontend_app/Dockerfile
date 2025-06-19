# ---------- build ----------
FROM node:20-alpine AS builder
WORKDIR /app

COPY frontend_app/package*.json .
RUN npm ci          # или pnpm / yarn

COPY frontend_app .
RUN npm run build   # vite → dist/

# ---------- runtime ----------
FROM nginx:1.25-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY frontend_app/docker/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
