import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


# Django command that pauses execution of a function
# until the database has been made available
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Database: Please wait, I am loading...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write(
                    'Database: Sorry, I am not available, I\'ll try again in \
one second...'
                    )
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database: I am now available!'))
