from django.core.management.base import BaseCommand
from spares.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Order.objects.all().delete()
        Spare.objects.all().delete()