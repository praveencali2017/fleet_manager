from django.shortcuts import render
from django.http.response import HttpResponse
from loguru import logger
from django.views.decorators.http import require_http_methods
# Create your views here.


@require_http_methods(['GET', 'POST'])
def file_upload(request):
    from feed_processor.tasks import task_read_and_send_to_topic
    from feed_processor.utils import ConsumerTopic
    from file_manager.constants import SupportedFile
    from file_manager.utils import save_in_memory_file
    from fleetmanager.settings import TMP_DIR_PATH
    upload_status = {'status': f'Nothing has been uploaded yet!!!'}
    if request.method == 'POST':
        file_data = request.FILES['file']
        supported_file_types = [file_type.value for file_type in SupportedFile]
        path = None
        if not file_data or file_data.content_type not in supported_file_types:
            msg = f'No file or file content not supported by the system!!!'
            logger.error(msg)
        else:
            path = save_in_memory_file(TMP_DIR_PATH, file_data)
        if path is None:
            msg = f'cannot process the file!!! Try again'
            upload_status['status'] = msg
            return render(request, "file_uploader.html", context=upload_status)
        upload_status['status'] = f'Failed to upload {file_data} !!! .'
        if file_data.content_type == SupportedFile.TXT_CSV.value:
            task_read_and_send_to_topic.delay(ConsumerTopic.VEHICLE_TIRE_PRESSURE_CU.value,
                                              path=path)
            upload_status['status'] = f'{file_data} has been uploaded!!!'
        # Todo: Just for simplicity, usually this data will be a server-server communication
        # available in message channels
        elif file_data.content_type == SupportedFile.APP_JSON.value:
            logger.info(SupportedFile.APP_JSON.value)
            task_read_and_send_to_topic.delay(ConsumerTopic.VEHICLE_BAT_FUEL_GEO_CU.value,
                                              path=path)
            upload_status['status'] = f'{file_data} has been uploaded!!!'
        else:
            upload_status['status'] = f'Failed!!! {file_data} is not supported.'
    return render(request, "file_uploader.html", context=upload_status)
