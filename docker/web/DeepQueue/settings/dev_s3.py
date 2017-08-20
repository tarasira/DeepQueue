from .base import *

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

# Use AWS S3 as the storage backend.
# Make sure to have
# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY for environment variables.
# AWS_STORAGE_BUCKET_NAME can also be set, but down here give a default value
# to it.
#
# The following environment variables should work.
# It can be tested by `python manage.py createfile`
#DJANGO_SETTINGS_MODULE="DeepQueue.settings.dev_s3"
#AWS_ACCESS_KEY_ID="aws_id"
#AWS_SECRET_ACCESS_KEY="aws_secret"
MEDIA_ROOT = '/media/'
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'tu-deep-queue-3')
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = S3_URL + MEDIA_ROOT

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
