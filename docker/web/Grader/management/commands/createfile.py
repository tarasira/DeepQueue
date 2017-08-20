import datetime

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create a test file on AWS S3'

    def handle(self, *args, **options):
        name = '{}-testfile.txt'.format(datetime.datetime.now().strftime('%S%M%H%d%m%Y'))
        f = default_storage.open(name, mode='w')
        f.write('A test text.')
        f.close()
