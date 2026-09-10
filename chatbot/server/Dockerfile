FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY . .

# Leads are stored as a JSON file under /app/data — mount a volume there so
# they survive container restarts/redeploys.
VOLUME ["/app/data"]

ENV PORT=3001
EXPOSE 3001

CMD ["node", "server.js"]
