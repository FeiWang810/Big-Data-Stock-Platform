# Store the data

## data-storage.py
receive data from kafka and store data in Cassandra.


### Dependencies
cassandra-driver    https://github.com/datastax/python-driver

cql

```sh
pip install -r requirements.txt
```

### Run
If your Cassandra run in a docker-machine named bigdata, and the ip of the virtual machine is 192.168.99.100

create keyspace and table using cqlsh.
```sh
CREATE KEYSPACE "stock" WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1} AND durable_writes = 'true';
USE stock;
CREATE TABLE stock (stock_symbol text, trade_time timestamp, trade_price float, PRIMARY KEY (stock_symbol,trade_time));
```

```sh
python data-storage.py stock-analyzer 192.168.99.100:9092 stock stock 192.168.99.100
```
