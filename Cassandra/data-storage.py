# read data from any kafka broker and topic
#write to any cassandra broker and topic

import argparse
from kafka import KafkaConsumer
from cassandra.cluster import  Cluster
import json
import logging
import atexit

logging.basicConfig()
logger=logging.getLogger('data-storage')
logger.setLevel(logging.DEBUG)

kafka_broker=''
kafka_topic=''
cassandra_broker=''
keyspace=''
table=''

def persist_data(stock_data, session):
	logger.debug('start to save data to cassandra %s' % stock_data)
	parsed = json.loads(stock_data)[0]
	symbol = parsed.get('StockSymbol')
	price = float(parsed.get('LastTradePrice'))
	tradetime = parsed.get('LastTradeDateTime')

	statement = "insert into %s (stock_symbol, trade_time, trade_price) values ('%s', '%s', %f)" % (table, symbol, tradetime, price)
	session.execute(statement)
	logger.debug('successfully save data to cassandra table')

def shutdown_hook(consumer,session):
    consumer.close()
    session.shutdown()
    logger.debug('resource released')

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('kafka_broker', help='the location of kafka broker')
    parser.add_argument('kafka_topic', help='the kafka topic')
    parser.add_argument('cassandra_broker', help='the location of cassandra')
    parser.add_argument('keyspace_name', help='the name of keyspace')
    parser.add_argument('table_name', help='the name of table')

    args = parser.parse_args()
    kafka_broker = args.kafka_broker
    kafka_topic = args.kafka_topic
    cassandra_broker = args.cassandra_broker
    keyspace = args.keyspace_name
    table = args.table_name

    #- instantiate kafka consumer
    consumer = KafkaConsumer(kafka_topic, bootstrap_servers=kafka_broker)

    #instantiate cassandra connection
    cassandra_connection=Cluster(contact_points=cassandra_broker.split(','))

    session = cassandra_connection.connect()

    session.execute("CREATE KEYSPACE IF NOT EXISTS %s WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} AND durable_writes = 'true'" % keyspace)
    session.set_keyspace(keyspace)
    session.execute("create table if not exists %s(stock_symbol text,trade_time timestamp,trade_price float, primary key(stock_symbol,trade_time))"% table)


    atexit.register(shutdown_hook,consumer,session)

    for msg in consumer:
        persist_data(msg.value, session)