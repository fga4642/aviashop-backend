from django.core.management import BaseCommand

from spares.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        CustomUser.objects.all().delete()

