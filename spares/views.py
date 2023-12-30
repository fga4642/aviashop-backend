from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializer import *


@api_view(["GET"])
def get_spares(request):
    spares = Spare.objects.all()
    serializer = SpareSerializer(spares, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def search_spares(request):

    query = request.GET.get("query")

    spares = Spare.objects.filter(name__icontains=query).filter(status=1)

    serializer = SpareSerializer(spares, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_spare(request, pk):
    if not Spare.objects.filter(pk=pk).exists():
        return Response(f"Авизапчасти с таким id не существует!")

    spare = Spare.objects.get(pk=pk)
    serializer = SpareSerializer(spare, many=False)

    return Response(serializer.data)


@api_view(["GET"])
def get_spare_image(request, pk):
    if not Spare.objects.filter(pk=pk).exists():
        return Response(f"Авизапчасти с таким id не существует!")

    spare = Spare.objects.get(pk=pk)

    return HttpResponse(spare.image, content_type="image/png")


@api_view(["PUT"])
def update_spare(request, pk):
    if not Spare.objects.filter(pk=pk).exists():
        return Response(f"Авизапчасти с таким id не существует!")

    spare = Spare.objects.get(pk=pk)
    serializer = SpareSerializer(spare, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_spare(request):
    Spare.objects.create()

    spares = Spare.objects.all()
    serializer = SpareSerializer(spares, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_spare(request, pk):
    if not Spare.objects.filter(pk=pk).exists():
        return Response(f"Авиазапчасти с таким id не существует!")

    spare = Spare.objects.get(pk=pk)
    spare.status = 2
    spare.save()

    spares = Spare.objects.filter(status=1)
    serializer = SpareSerializer(spares, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def add_to_order(request, pk):
    if not Spare.objects.filter(pk=pk).exists():
        return Response(f"Авиазапчасти с таким id не существует!")

    spare = Spare.objects.get(pk=pk)

    order = Order.objects.filter(status=1).last()

    if order is None:
        order = Order.objects.create()

    order.spares.add(spare)

    order.save()

    serializer = SpareSerializer(order.spares, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_order(request, pk):
    if not Order.objects.filter(pk=pk).exists():
        return Response(f"Заказа с таким id не существует!")

    order = Order.objects.get(pk=pk)
    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_order(request, pk):
    if not Order.objects.filter(pk=pk).exists():
        return Response(f"Заказа с таким id не существует!")

    order = Order.objects.get(pk=pk)
    serializer = OrderSerializer(order, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_order_user(request, pk):
    if not Order.objects.filter(pk=pk).exists():
        return Response(f"Заказа с таким id не существует!")

    request_status = request.data["status"]

    if request_status not in [1, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order = Order.objects.get(pk=pk)
    order_status = order.status

    if order_status == 5:
        return Response("Статус изменить нельзя")

    order.status = request_status
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_order_admin(request, pk):
    if not Order.objects.filter(pk=pk).exists():
        return Response(f"Заказа с таким id не существует!")

    request_status = request.data["status"]

    if request_status in [1, 5]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order = Order.objects.get(pk=pk)
    order_status = order.status

    if order_status not in [1]:
        return Response("Статус изменить нельзя")

    order.status = request_status
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_order(request, pk):
    if not Order.objects.filter(pk=pk).exists():
        return Response(f"Заказа с таким id не существует!")

    order = Order.objects.get(pk=pk)
    order.status = 2
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["POST"])
def add_spare_to_order(request, order_id, spare_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(f"Заказа с таким id не существует")

    if not Spare.objects.filter(pk=spare_id).exists():
        return Response(f"Авиазапчасти с таким id не существует")

    order = Order.objects.get(pk=order_id)
    order.spares.add(Spare.objects.get(pk=spare_id))
    order.save()

    serializer = SpareSerializer(order.spares, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_spare_from_order(request, order_id, spare_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(f"Заказа с таким id не существует")

    if not Spare.objects.filter(pk=spare_id).exists():
        return Response(f"Авиазапчасти с таким id не существует")

    order = Order.objects.get(pk=order_id)
    order.spares.remove(Spare.objects.get(pk=spare_id))
    order.save()

    serializer = SpareSerializer(order.spares, many=True)

    return Response(serializer.data)
