FROM node:current
RUN npm install -qg http-server
WORKDIR /deep-stock-frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN echo "export const backendUrl = 'https://backend-dot-deep-stock-268818.appspot.com'" > ./src/variables.js
RUN npm run build
EXPOSE 8080
CMD ["http-server", "dist"]
