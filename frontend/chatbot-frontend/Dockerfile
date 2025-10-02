# Stage 1: build
FROM node:20-alpine AS build
WORKDIR /app

# Copy package.json and lock file
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build Next.js app
RUN npm run build

# Stage 2: run
FROM node:20-alpine
WORKDIR /app
COPY --from=build /app ./
EXPOSE 3000

CMD ["npm", "start"]
