# Web

## index.js

Build a webpage shows the real-time procesed stock data.

### Dependencies
socket.io       http://socket.io/

redis           https://www.npmjs.com/package/redis

smoothie        https://www.npmjs.com/package/smoothie

minimist        https://www.npmjs.com/package/minimist

```sh
npm install
```

### Run
If your all your application run in a docker-machine named bigdata, and the ip of the virtual machine is 192.168.99.100
```sh
node index.js --port=3000 --redis_host=192.168.99.100 --redis_port=6379 --subscribe_topic=average-stock-price
```
![image](https://github.com/FeiWang810/Big-Data-Stock-Platform/blob/master/images/Nodejs.png)
