#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 12:28:55 2017

@author: feiwang
"""

import argparse
import atexit
import json
from googlefinance import getQuotes

from kafka import KafkaProducer
from kafka.errors import KafkaError
from apscheduler.schedulers.background import BackgroundScheduler

import  logging
logging.basicConfig()
logger=logging.getLogger('Assignment2')

logger.setLevel(logging.DEBUG)
schedule=BackgroundScheduler()
schedule.add_executor('threadpool')
schedule.start()

kafka_broker=''
topic_name=''
def shutdown_hook(producer):
    producer.flush(3)
    producer.close()
    logger.info("kafka producer coonextion closed")
    schedule.shutdown()
    logger.info('threadpoll released')




def fetch_price(producer,symbol):
    try:
        logger.debug('start to get stock price for %s', symbol)
        price = json.dumps(getQuotes(symbol))
        logger.debug('retrieved stock into %s', price)
        producer.send(topic=topic_name, value=price)
        logger.debug('sent stock price for %s', symbol)
    except KafkaError as ke:
        logger.warn('fail to send data to kafka')
    except Exception as e:
        logger.error('fail to fetch the price for %s',symbol)
        
if __name__=='__main__':
    parser= argparse.ArgumentParser()
    parser.add_argument('symbol',help="the symbol of the stock")
    parser.add_argument('topic_name',help="the kafka topic")
    parser.add_argument('kafka_broker',help='the location of kafka broker')

    args=parser.parse_args()
    symbol=args.symbol
    topic_name=args.topic_name
    kafka_broker=args.kafka_broker

    price=json.dumps(getQuotes(symbol))

    producer=KafkaProducer(bootstrap_servers=kafka_broker)

    schedule.add_job(fetch_price,'interval',[producer,symbol],seconds=1)


    while True:
        pass

    atexit.register(shutdown_hook,producer)

