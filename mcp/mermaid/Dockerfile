FROM node:20-alpine

WORKDIR /app
RUN npm install -g @mermaid-js/mermaid-cli

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy project files
COPY . .

# Expose port and start
EXPOSE 8000
CMD ["npm", "run", "start_v2"]



# FROM node:20-alpine
# WORKDIR /app

# # Install dependencies
# COPY package.json package-lock.json* ./
# RUN npm install --production

# # Copy project files
# COPY . .

# # Expose port and start
# EXPOSE 8000
# CMD ["npm", "start"]