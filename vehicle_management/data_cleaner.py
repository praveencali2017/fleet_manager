"""
Helper functions to convert data to data suitable for models
"""

from loguru import logger


def transform_csv_vehicle_data(data: dict):
    """
    vehicle dict data and clean the data for ingestion to models
    :return:
    """
    try:
        tires = list(filter(lambda x: 'tires' in x, data.keys()))
        tire_data = dict()
        for tire_key in tires:
            tire_key_format = tire_key.replace("/", "_")
            tire_data.update({tire_key_format: data.pop(tire_key)})
        data['tires'] = tire_data
        return data
    except Exception as e:
        logger.error(f'[transform_csv_vehicle_data]>>>> {str(e)}')


def ingest_data_to_vehicle_status(record: dict):
    from vehicle_management.models import VehicleStatus, VEHICLESTATUS_PK
    try:
        VehicleStatus.create_or_update_vehicle(**record, key_identifiers=[VEHICLESTATUS_PK])
    except Exception as e:
        logger.error(f'ingest_data_to_vehicle_status>>>> {str(e)}')




# transform_csv_vehicle_data(test_byte)