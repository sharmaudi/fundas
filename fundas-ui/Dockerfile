FROM node:8

WORKDIR /app

ADD package.json /app/package.json
RUN npm install
RUN npm install react-paginate --save
ADD . /app

EXPOSE 3000
EXPOSE 35729

CMD [ "npm", "start" ]