from fleetmanager import celery_app


@celery_app.task
def task_read_and_send_to_topic(topic, path):
    """
    Background task to read and publish data to messaging channel
    :param topic: topic of (publish/subscribe)
    :param path: path of the file
    :return: None
    """
    from feed_processor.file_processor import read_file_and_send_to_topic
    from feed_processor.utils import ConsumerTopic
    from loguru import logger
    logger.info(f'task_read_and_send_to_topic >>>sending data for topic: {topic}')
    if topic == ConsumerTopic.VEHICLE_TIRE_PRESSURE_CU.value:
        logger.info("read file send")
        read_file_and_send_to_topic(topic, path, 'csv')
    if topic == ConsumerTopic.VEHICLE_BAT_FUEL_GEO_CU.value:
        read_file_and_send_to_topic(topic, path, 'json')
