FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm config set registry https://registry.npmjs.org/
RUN npm install

COPY . .

CMD ["npm", "start"]