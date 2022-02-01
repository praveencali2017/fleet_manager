import os.path

import pandas as pd
from loguru import logger


def read_csv_data(path: str):
    """
    Reads the csv from the given path and convert it to a dict of records(list)
    :param path: path of the file
    :return: dict of records
    """
    if not path.endswith('.csv'):
        logger.info(f'File at {path} is not a csv!!!')
        return
    data_df = pd.read_csv(path)
    data_dict = data_df.to_dict(orient='records')
    return data_dict


def read_file_and_send_to_topic(topic, path, file_type):
    """
    Reads csv/json array file given path and sends to the message channel
    :param topic: topic/channel of the publisher-subscriber
    :param path: path to the file
    :return: None
    """
    from feed_processor.topic_sender import send_data_msg_channel
    import json
    data = None
    if file_type == 'csv':
        data = read_csv_data(path=path)
    if file_type == 'json':
        data = json.load(open(path, 'rb'))
    if not data:
        return
    logger.info(f'sending for channel {topic} >>>')
    for record in data:
        msg = json.dumps(record)
        logger.info(msg)
        send_data_msg_channel(topic=topic, message=msg)

