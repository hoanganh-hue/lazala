# Backend Dockerfile (Node JS runtime, no tsx in production)

# ---------- Build stage: compile TypeScript to JavaScript ----------
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package & tsconfig
COPY package*.json ./
COPY tsconfig.json ./
COPY tsconfig.build.json ./

# Install full deps (incl. dev) to compile
RUN npm ci && npm cache clean --force

# Copy sources
COPY server/ ./server/
COPY shared/ ./shared/

# Compile to dist/ using tsc (tsconfig.build.json)
RUN npx tsc -p tsconfig.build.json

# ---------- Runtime stage: run compiled JS with Node ----------
FROM node:20-alpine
WORKDIR /app

# Install only production dependencies
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

# Copy compiled output from builder
COPY --from=builder /app/dist ./dist

# Create necessary directories
RUN mkdir -p /app/uploads /app/logs

# Set environment variables
ENV NODE_ENV=production
ENV PORT=5000

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:5000/api/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Run migrations and start server (compiled JS)
CMD ["sh", "-c", "node dist/server/scripts/migrate.js && node dist/server/index.js"]

