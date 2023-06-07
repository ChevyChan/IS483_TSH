FROM node:lts-alpine

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./

RUN npm install --production --silent && mv node_modules ../

COPY . .

CMD ["npm", "start"]