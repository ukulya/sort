import os
from urllib.parse import urljoin

DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
# MINIO STORAGE

DEFAULT_FILE_STORAGE = 'minio_storage.storage.MinioMediaStorage'
STATICFILES_STORAGE = 'minio_storage.storage.MinioStaticStorage'
MINIO_STORAGE_ACCESS_KEY = os.environ['MINIO_ACCESS_KEY']
MINIO_STORAGE_SECRET_KEY = os.environ['MINIO_SECRET_KEY']
MINIO_STORAGE_ENDPOINT = os.environ['MINIO_INTERNAL_HOST']
DEFAULT_STORAGE_ENDPOINT = os.environ['MINIO_ENDPOINT_HOST']
MINIO_STORAGE_MEDIA_BUCKET_NAME = 'main-backend-media'
MINIO_STORAGE_STATIC_BUCKET_NAME = 'main-backend-static'
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True
MINIO_STORAGE_AUTO_CREATE_STATIC_BUCKET = True
MINIO_STORAGE_STATIC_URL = urljoin(
    DEFAULT_STORAGE_ENDPOINT, MINIO_STORAGE_STATIC_BUCKET_NAME
)
MINIO_STORAGE_MEDIA_URL = urljoin(
    DEFAULT_STORAGE_ENDPOINT, MINIO_STORAGE_MEDIA_BUCKET_NAME
)
MINIO_STORAGE_MEDIA_USE_PRESIGNED = False
MINIO_STORAGE_USE_HTTPS = False
MINIO_STORAGE_AUTO_CREATE_MEDIA_POLICY = "READ_ONLY"
