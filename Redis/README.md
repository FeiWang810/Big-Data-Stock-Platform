# Cache the data

## redis-producer.py
Redis producer:consume message from kafka and publish to redis PUB.


### Dependencies
kafka-python    https://github.com/dpkp/kafka-python

redis           https://pypi.python.org/pypi/redis

```sh
pip install -r requirements.txt
```

### Run
If your Redis run in a docker-machine named bigdata, and the ip of the virtual machine is 192.168.99.100
```sh
python redis-publisher.py average-stock-price 192.168.99.100:9092 average-stock-price 192.168.99.100 6379

The first average-stock-price is my kafka topic.

The first IP address is my docker-machine address.

The second average-stock-price is my redis channel followed by redis host and redis port.
```
![image](https://github.com/FeiWang810/Big-Data-Stock-Platform/blob/master/images/Redis.png)
