from datetime import datetime
import logging
import multiprocessing
import threading

from locust import events
import pika
from pika.exceptions import AMQPError


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)


class RabbitMQClient(object):
    _connected = False

    def __init__(self):
        self._process_name = multiprocessing.current_process().name
        self._thread_name = threading.current_thread().name
        self._connection = None
        self._channel = None

    def connect(self):
        params = pika.URLParameters('amqp://192.168.99.100')
        self._connection = pika.BlockingConnection(params)
        self._channel = self._connection.channel()
        self._connected = True

    def publish(self, exchange, routing_key, message):
        """
        Constructs and publishes a simple message
        via amqp.basic_publish
        :param message: the message consumed by data-collection, in a json format
        :param exchange: the name of the exchange
        :param routing_key: the name of the routing key
        """
        if not self._connected:
            self.connect()

        try:
            self._channel.basic_publish(exchange, routing_key, message)
        except AMQPError as e:
            events.request_failure.fire(
                request_type="BASIC_PUBLISH",
                name="test.message",
                exception=e,
            )
        else:
            events.request_success.fire(
                request_type="BASIC_PUBLISH",
                name="test.message",
                response_length=0
            )

    def close_channel(self):
        if self._channel is not None:
            LOGGER.info('Closing the channel')
            self._channel.close()

    def close_connection(self):
        if self._connection is not None:
            LOGGER.info('Closing connection')
            self._connection.close()

    def disconnect(self):
        self.close_channel()
        self.close_connection()
        self._connected = False


client = None


def get_client():
    global client
    if client is None:
        client = RabbitMQClient()
    return client
