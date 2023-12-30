import random
from tqdm import tqdm

from django.core import management
from django.core.management.base import BaseCommand
from spares.models import *
from .utils import random_date, random_timedelta


def add_spares(count):
    last_spare_id = 1
    if Spare.objects.count() > 0:
        last_spare_id = Spare.objects.last().id + 1

    for _ in range(count):
        Spare.objects.create(
            name=f"Авиазапчасть №{last_spare_id}",
            image=f"spares/{random.randint(1,4)}.jpg",
            price=random.randint(1000, 50000),
            weight=random.randint(1, 500),
            rating=round(random.uniform(1.0, 5.0), 1)
        )

        last_spare_id += 1

    print("Услуги добавлены")


def add_orders(count):
    owners = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(owners) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    spares = Spare.objects.all()

    for _ in tqdm(range(count)):
        order = Order.objects.create()
        order.status = random.randint(2, 5)

        if order.status in [3, 4]:
            order.closed_date = random_date()
            order.date_of_formation = order.closed_date - random_timedelta()
            order.created_date = order.date_of_formation - random_timedelta()
            order.moderator = random.choice(moderators)
        else:
            order.date_of_formation = random_date()
            order.created_date = order.date_of_formation - random_timedelta()

        order.owner = random.choice(owners)

        for i in range(random.randint(1, 3)):
            order.spares.add(random.choice(spares))

        order.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='+', type=int, help='Ratio value')

    def handle(self, *args, **kwargs):
        management.call_command("clean_db")

        ratio = kwargs['ratio'][0]

        add_spares(10 * ratio)
        add_orders(100 * ratio)









