from loguru import logger
class BaseMethod:
    @classmethod
    def create_or_update(cls, key_identifiers: list, **kwargs):
        """
        Create or update model data, based on key_identifiers match. Updates values supplied in kwargs
        :param key_identifiers: matching keys
        :param kwargs: to be updated values
        :return: tuple (instance, True/False: created or not)
        """
        match_identifiers = dict()
        column_data = {**kwargs}
        for key in key_identifiers:
            if key in kwargs:
                match_identifiers[key] = kwargs.pop(key)
            else:
                match_identifiers[key] = None
        # Filter for attributes not equal to model name before insertion or update
        for key in kwargs:
            if key not in cls.__dict__:
                column_data.pop(key)
        logger.info(f"update or create >>>>{match_identifiers}")
        logger.info(f"update or create >>>>{column_data}")
        instance, created = cls.objects.update_or_create(**match_identifiers, defaults=column_data)
        return instance, created

    @classmethod
    def get_all(cls, **filters):
        try:
            instances = cls.objects.filter(**filters).all()
            return instances
        except cls.DoesNotExist as e:
            logger.error(f'{cls.__name__} model instance for the filters, does not exists!!!')
            return []

    @classmethod
    def get_count(cls, **filters):
        return cls.objects.filter(**filters).count()

    @classmethod
    def get_all_Q(cls, *args):
        try:
            instances = cls.objects.filter(*args).all()
            return instances
        except cls.DoesNotExist as e:
            logger.error(f'{cls.__name__} model instance for the filters, does not exists!!!')
            return []

    @classmethod
    def get(cls, **filters):
        try:
            instance = cls.objects.filter(**filters).get()
            return instance
        except cls.DoesNotExist as e:
            logger.error(f'{cls.__name__} model instance for the filters, does not exists!!!')
            return None

    @classmethod
    def delete_objects(cls, **filters):
        rows_deleted, _ = cls.objects.filter(**filters).delete()
        if rows_deleted >= 1:
            return True
        return False


