import random
from tqdm import tqdm

from django.core import management
from django.core.management.base import BaseCommand
from spares.models import *
from .utils import random_date, random_timedelta, random_text


# def add_spares(count):
#     last_spare_id = 1
#     if Spare.objects.count() > 0:
#         last_spare_id = Spare.objects.last().id + 1
#
#     for _ in range(count):
#         Spare.objects.create(
#             name=f"Авиазапчасть №{last_spare_id}",
#             description=random_text(15),
#             image=f"spares/{random.randint(1, 4)}.jpg",
#             price=random.randint(1000, 50000),
#             weight=random.randint(1, 500),
#             rating=round(random.uniform(1.0, 5.0), 1)
#         )
#
#         last_spare_id += 1
#
#     print("Услуги добавлены")

def add_spares(count):
    Spare.objects.create(
        name=f"Насос ЭЦН-109а с электродвигателем ГЭА-6А",
        description="""Новые! Упаковки, коробки, паспорта, ярлыки консервации, хранение - сухой склад!
 6шт. цена за шт.
 За опт - скидка!""",
        image=f"spares/1.jpg",
        price=random.randint(1000, 50000),
        weight=random.randint(1, 500),
        rating=round(random.uniform(1.0, 5.0), 1)
    )

    Spare.objects.create(
        name=f"Двигатель РУ 19-300",
        description="""После ремонта. ППР- 0 ч.
Без формуляра. С официальным происхождением.
Турбореактивный двигатель РУ 19-300 предназначен для установки на самолете в качестве дополнительной энергоустановки.""",
        image=f"spares/2.jpg",
        price=random.randint(1000, 50000),
        weight=random.randint(1, 500),
        rating=round(random.uniform(1.0, 5.0), 1)
    )

    Spare.objects.create(
        name=f"Авиагоризонт АГБ-2",
        description="""Подойдет для реализации проектов: авиатренажер, авиасимулятор, развлекательный аттракцион, или любой другой.
Boeing 737 — узкофюзеляжный ближне-среднемагистральный пассажирский самолёт.""",
        image=f"spares/3.jpg",
        price=random.randint(1000, 50000),
        weight=random.randint(1, 500),
        rating=round(random.uniform(1.0, 5.0), 1)
    )

    Spare.objects.create(
        name=f"Кабина самолета Ан-32",
        description="Новый, с хранения, пломбы целые. Картонная упаковка и паспорт утрачены в процессе хранения.",
        image=f"spares/4.jpg",
        price=random.randint(1000, 50000),
        weight=random.randint(1, 500),
        rating=round(random.uniform(1.0, 5.0), 1)
    )

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
        order.owner = random.choice(owners)

        if order.status in [2, 3, 4]:
            order.delivery_date = random.randint(7, 14)

        if order.status in [3, 4]:
            order.closed_date = random_date()
            order.date_formation = order.closed_date - random_timedelta()
            order.created_date = order.date_formation - random_timedelta()
            order.moderator = random.choice(moderators)
        else:
            order.date_formation = random_date()
            order.created_date = order.date_formation - random_timedelta()

        for i in range(random.randint(1, 3)):
            order.spares.add(random.choice(spares))

        order.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', nargs='+', type=int, help='Ratio value')

    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        ratio = kwargs['ratio'][0]

        add_spares(10 * ratio)
        add_orders(100 * ratio)









