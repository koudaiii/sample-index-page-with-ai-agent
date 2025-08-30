FROM node:24-alpine

WORKDIR /app

# Copy only package files first to leverage cache
COPY package.json package-lock.json ./

# Install dependencies (including dev dependencies for Vite dev server)
RUN npm ci

# Copy application source
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs

# Change ownership of the app directory
RUN chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Expose port 5000 (Vite dev server default)
EXPOSE 5000

# Start Vite dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
