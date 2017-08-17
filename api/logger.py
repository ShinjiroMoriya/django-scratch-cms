from logging import getLogger
from django.conf import settings

logger = getLogger('command')

__all__ = ('logger',)


def logger_info(value):
    if settings.DEV:
        logger.info(value)
    return None
