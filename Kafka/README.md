# Send data to Kafka Broker

## Install Dependencies
```sh
pip install -r requirements.txt
```

## simple-data-producer.py
A data producr which can grasp stock data each second and sent to kafka

### Dependencies
googlefinance   https://pypi.python.org/pypi/googlefinance
kafka-python    https://github.com/dpkp/kafka-python
schedule        https://pypi.python.org/pypi/schedule

### Run
If your Kafka run in a docker-machine named bigdata, and the ip of the virtual machine is 192.168.99.100
```sh
python producer.py AAPL stock-analyzer 192.168.99.100:9092
```

### Run flask-data-producer
加入你的Kafka运行在一个叫做bigdata的docker-machine里面, 然后虚拟机的ip是192.168.99.100
```sh
export ENV_CONFIG_FILE=`pwd`/config/dev.cfg
python flask-data-producer.py
```
