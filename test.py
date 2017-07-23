#!/usr/bin/env python
import threading, logging, time
import multiprocessing

from kafka import KafkaConsumer, KafkaProducer


class Producer(threading.Thread):
    daemon = True

    def run(self):
        producer = KafkaProducer(bootstrap_servers='192.168.1.64:9092')

        while True:
            producer.send('test', b"\xc2Hello, world!")
            time.sleep(1)


class Consumer(multiprocessing.Process):
    daemon = True

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='192.168.1.64:9092',
                                 auto_offset_reset='earliest')
        consumer.subscribe(['test'])

        for message in consumer:
            print (message)


def main():
    tasks = [
        Producer(),
        Consumer()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
        )
    main()

