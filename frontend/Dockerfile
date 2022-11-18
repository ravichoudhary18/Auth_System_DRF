FROM node:16-alpine3.14
WORKDIR /home/node
COPY package.json ./
# COPY package-lock.json ./
RUN npm install
RUN npm install react-scripts@3.4.1
COPY . .
RUN chown -R node:node node_modules
CMD npm start
