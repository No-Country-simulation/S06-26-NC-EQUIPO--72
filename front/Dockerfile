FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN apk add --no-cache libc6-compat
RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]