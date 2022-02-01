def save_in_memory_file(dir_path, file):
    """
    Saves the inmemory file inside the given dir_path
    :param dir_path: path towards the dir
    :param file: file to be saved
    :return: path of the file
    """
    import os
    from django.core.files.base import ContentFile
    from django.core.files.storage import default_storage
    path = os.path.join(dir_path, file.name)
    _ = default_storage.save(path, ContentFile(file.read()))
    return path