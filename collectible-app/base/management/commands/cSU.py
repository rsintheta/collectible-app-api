from django.contrib.auth import get_user_model as gum
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        if gum().objects.filter(
            email=os.environ.get(
                'DJANGO_SUPERUSER_EMAIL')
                ).count() == 0:
            print('creating')
            gum().objects.create_superuser(
                email=os.environ.get('DJANGO_SUPERUSER_EMAIL'),
                password=os.environ.get('DJANGO_SUPERUSER_PASSWORD'),
                name=os.environ.get('DJANGO_SUPERUSER_USERNAME'),
                )
        else:
            print('existing')
