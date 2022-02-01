from feed_processor.utils import ConsumerTopic
from feed_processor.vehicle_data_listener import pubsub


def send_data_msg_channel(topic, message):
    if topic == ConsumerTopic.VEHICLE_TIRE_PRESSURE_CU.value:
        pubsub.publish(ConsumerTopic.VEHICLE_TIRE_PRESSURE_CU.value, message)
    elif topic == ConsumerTopic.VEHICLE_BAT_FUEL_GEO_CU.value:
        pubsub.publish(ConsumerTopic.VEHICLE_BAT_FUEL_GEO_CU.value, message)
