import random
from datetime import datetime, timedelta
from django.utils import timezone

from spares.jwt_helper import get_access_token, get_jwt_payload
from spares.models import CustomUser


def random_date():
    now = datetime.now(tz=timezone.utc)
    return now + timedelta(random.uniform(-1, 0) * 100)


def random_timedelta(factor=100):
    return timedelta(random.uniform(0, 1) * factor)


def identity_user(request):
    access_token = get_access_token(request)

    if access_token is None:
        return None

    payload = get_jwt_payload(access_token)
    user_id = payload["user_id"]
    user = CustomUser.objects.get(pk=user_id)

    return user


def random_text(maxlen=10):
    words = ["lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "cras", "eu", "blandit",
           "lacus",  "vivamus", "tincidunt", "ante", "nec", "nunc", "tincidunt", "lacinia", "curabitur", "maximus",
           "vulputate", "nisi", "vitae", "bibendum"]

    text = ""

    for _ in range(random.randint(1, maxlen)):
        text += random.choice(words) + " "

    text = text.strip().replace(text[0], text[0].upper(), 1)

    return text