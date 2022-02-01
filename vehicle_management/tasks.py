from fleetmanager import celery_app


@celery_app.task
def task_vehicle_status_model_update(data, file_type):
    """
    Background task to create or update vehicle data to data model
    :param data: uncleaned vehicle data
    :param file_type: csv/json
    :return: None
    """
    from vehicle_management.data_cleaner import transform_csv_vehicle_data, ingest_data_to_vehicle_status
    vehicle_data = data
    if file_type == 'csv':
        vehicle_data = transform_csv_vehicle_data(data=data)
    ingest_data_to_vehicle_status(vehicle_data)