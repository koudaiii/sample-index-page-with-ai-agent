FROM node:24-alpine AS builder

WORKDIR /app

# Copy only package files first to leverage cache
COPY package.json package-lock.json ./

# Install dependencies (dev deps needed for build)
RUN npm ci

# Copy only necessary app sources
COPY index.html ./
COPY vite.config.ts tsconfig.json tailwind.config.js components.json ./
COPY src ./src

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine AS production

# Copy custom nginx configuration
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

# Copy built application from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Set permissions for nginx to run as non-root
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx && \
    chown -R nginx:nginx /var/log/nginx && \
    chown -R nginx:nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid && \
    chmod 755 /var/cache/nginx /var/log/nginx

# Expose port 8080
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
