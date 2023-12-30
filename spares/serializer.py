from rest_framework import serializers

from .models import *


class SpareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spare
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

