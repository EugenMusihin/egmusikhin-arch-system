FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install -g yarn
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
RUN npm install

COPY . .

CMD ["npm", "start"]