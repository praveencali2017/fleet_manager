import redis
from fleetmanager.settings import REDIS_HOST, REDIS_PORT
"""
Consumer base class, along with specific msg_pattern
"""


class PubSubMsgPattern:
    message_broker = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def __init__(self, name):
        self.name = name
        self.topic = None
        self.receiver = PubSubMsgPattern.message_broker.pubsub()

    def subscribe(self, topic):
        self.receiver.subscribe(topic)

    def publish(self, topic, message):
        PubSubMsgPattern.message_broker.publish(topic, message=message)



