# Frontend Dockerfile
FROM node:18

WORKDIR /usr/src/app

COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

#CMD ["npm", "start"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
