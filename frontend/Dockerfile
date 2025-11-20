# Stage 1: build
FROM node:18 AS builder
WORKDIR /app
# Copy package files first for better layer caching
COPY package.json package-lock.json* ./
# If using pnpm/yarn, adapt accordingly
RUN npm ci --silent
COPY . .
RUN npm run build


# Stage 2: runtime
FROM nginx:alpine
# Remove default static files
RUN rm -rf /usr/share/nginx/html/*
# Copy built static files from builder
COPY --from=builder /app/dist /usr/share/nginx/html
# Copy custom nginx config (for SPA routing)
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]