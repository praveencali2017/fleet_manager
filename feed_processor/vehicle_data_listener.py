from msg_pattern.pub_sub_msg_pattern import PubSubMsgPattern
from feed_processor.utils import ConsumerTopic
from loguru import logger
# Define a global vehicle data consumer
pubsub = PubSubMsgPattern(name='vehicle_data')

# Extract all topics from defined enum
topics = [topic.value for topic in ConsumerTopic]

# Subscribe for all topics
for topic in topics:
    pubsub.subscribe(topic=topic)

# Should run as a separate process!!!
if __name__ == '__main__':
    import json
    from vehicle_management.tasks import task_vehicle_status_model_update
    logger.info(f'listening for topics: {topics}')
    while True:
        response = pubsub.receiver.get_message()
        if response is None:
            continue
        elif response['type'] == 'subscribe':
            continue
        elif 'data' not in response:
            continue
        elif type(response['data']) == int:
            continue
        elif response['type'] == 'message':
            data = response['data']
            channel = response['channel'].decode('utf-8')
            if channel == ConsumerTopic.VEHICLE_TIRE_PRESSURE_CU.value:
                vehicle_data = json.loads(data)
                task_vehicle_status_model_update.delay(vehicle_data, 'csv')
            if channel == ConsumerTopic.VEHICLE_BAT_FUEL_GEO_CU.value:
                vehicle_data = json.loads(data)
                task_vehicle_status_model_update.delay(vehicle_data, 'json')




