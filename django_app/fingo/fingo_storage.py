from django.conf import settings
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    location = settings.STATIC_FILE_LOCATION


class MediaStorage(S3BotoStorage):
    location = settings.MEDIA_FILE_LOCATION