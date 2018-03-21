#-read from any kafka topic and cluster
#-do data processing using spark streaming
#-write data back to kafka

import argparse
import logging
import json
import atexit

from kafka import KafkaProducer
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


logging.basicConfig()
logger=logging.getLogger('data-processing')
logger.setLevel(logging.INFO)

kafka_producer=None
new_topic=None

def shutdown_hook(producer):
    producer.flush(10)
    logger.info('closed kafka producer')
    producer.close(10)

def process_stream(stream):

    def write_to_kafka(rdd):
        result=rdd.collect()
        for r in result:
            data=json.dumps({'symbol':r[0],'average':r[1]})
            logger.info('sending average price %s to kafka'%data)
            kafka_producer.send(new_topic,value=data)

    def pair(data):
        record=json.loads(data[1].decode('utf-8'))[0]
        return record.get('StockSymbol'),(float(record.get('LastTradePrice')),1)


    stream.map(pair).reduceByKey(lambda a,b: (a[0]+b[0],a[1]+b[1])).map(lambda(k,v):(k,v[0]/v[1])).foreachRDD(write_to_kafka)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('topic',help='the kafka topic to read from')
    parser.add_argument('new_topic',help='the new kafka topic')
    parser.add_argument('broker',help='the kafka broker location')

    args=parser.parse_args()
    topic=args.topic
    new_topic=args.new_topic
    broker=args.broker

    sc=SparkContext('local[2]','stock_average_price')
    sc.setLogLevel('ERROR')
    ssc=StreamingContext(sc,5)

    directKafkaStream=KafkaUtils.createDirectStream(ssc,[topic],{'metadata.broker.list':broker})
    process_stream(directKafkaStream)

    kafka_producer=KafkaProducer(bootstrap_servers=broker)

    atexit.register(shutdown_hook,kafka_producer)

    ssc.start()
    ssc.awaitTermination()


