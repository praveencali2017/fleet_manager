celery_worker: celery -A fleetmanager worker --loglevel=INFO
celery_beat: celery -A fleetmanager beat -l info
vehicle_listener: PYTHONPATH=. python feed_processor/vehicle_data_listener.py
web_server: PYTHONPATH=. python manage.py runserver