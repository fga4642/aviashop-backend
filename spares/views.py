from datetime import datetime

import requests
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import create_access_token
from .management.commands.utils import identity_user
from .permissions import *
from .serializer import *


def get_draft_order(request):
    user = identity_user(request)

    if user is None:
        return None

    order = Order.objects.filter(owner_id=user.pk).filter(status=1).first()

    return order


@api_view(["GET"])
def search_spares(request):
    query = request.GET.get("query", "")
    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", 5))

    spares = Spare.objects.filter(name__icontains=query).filter(status=1)

    serializer = SpareSerializer(spares[offset:offset + limit], many=True)

    draft_order = get_draft_order(request)
    data = {
        "spares": serializer.data,
        "draft_order_id": draft_order.pk if draft_order else None,
        "totalCount": len(spares)
    }

    return Response(data)


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
@permission_classes([IsModerator])
def update_spare(request, pk):
    if not Spare.objects.filter(pk=pk).exists():
        return Response(f"Авизапчасти с таким id не существует!")

    spare = Spare.objects.get(pk=pk)
    serializer = SpareSerializer(spare, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_spare(request):
    spare = Spare.objects.create()

    serializer = SpareSerializer(spare, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsModerator])
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
@permission_classes([IsAuthenticated])
def add_spare_to_order(request, spare_id):
    if not Spare.objects.filter(pk=spare_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    spare = Spare.objects.get(pk=spare_id)

    draft_order = get_draft_order(request)
    user = identity_user(request)

    if draft_order is None:
        draft_order = Order.objects.create()
        draft_order.owner = user
        draft_order.save()

    if draft_order.spares.contains(spare):
        return Response(status=status.HTTP_409_CONFLICT)

    draft_order.spares.add(spare)
    draft_order.owner = user
    draft_order.save()

    serializer = OrderSerializer(draft_order)

    return Response(serializer.data, status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_orders(request):
    user = identity_user(request)

    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get("limit", 5))
    status = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    orders = Order.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        orders = orders.filter(owner=user)

    if status > 0:
        orders = orders.filter(status=status)

    if date_start:
        orders = orders.filter(date_formation__gte=parse_datetime(date_start))

    if date_end:
        orders = orders.filter(date_formation__lte=parse_datetime(date_end))

    serializer = OrderSerializer(orders, many=True)

    resp = {
        "orders": serializer.data[offset:offset + limit],
        "totalCount": len(serializer.data)
    }

    return Response(resp)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order(request, pk):
    if not Order.objects.filter(pk=pk).exists():
        return Response(f"Заказа с таким id не существует!")

    order = Order.objects.get(pk=pk)
    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_order(request, pk):
    if not Order.objects.filter(pk=pk).exists():
        return Response(f"Заказа с таким id не существует!")

    order = Order.objects.get(pk=pk)
    serializer = OrderSerializer(order, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsRemoteWebService])
def update_order_delivery_date(request, pk):
    if not Order.objects.filter(pk=pk).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=pk)

    days = request.data.get("delivery_date", -1)
    if days > 0:
        order.delivery_date = days
        order.save()
        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_404_NOT_FOUND)


def calculate_order_delivery_date(order_id):
    data = {
        "order_id": order_id,
        "access_token": settings.REMOTE_WEB_SERVICE_AUTH_TOKEN,
    }

    requests.post("http://127.0.0.1:8080/calc_delivery_date/", json=data, timeout=3)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_order_user(request, pk):
    if not Order.objects.filter(pk=pk).exists():
        return Response(f"Заказа с таким id не существует!")

    order = Order.objects.get(pk=pk)
    order.status = 2
    order.date_formation = timezone.now()
    order.save()

    calculate_order_delivery_date(order.pk)

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_order_admin(request, pk):
    access_token = get_access_token(request)
    payload = get_jwt_payload(access_token)
    user_id = payload["user_id"]

    if not Order.objects.filter(pk=pk).exists():
        return Response(f"Заказа с таким id не существует!")

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order = Order.objects.get(pk=pk)
    order_status = order.status

    if order_status != 2:
        return Response("Статус изменить нельзя", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = request_status
    order.date_complete = timezone.now()
    order.moderator = CustomUser.objects.get(pk=user_id)
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    if not Order.objects.filter(pk=pk).exists():
        return Response(f"Заказа с таким id не существует!")

    order = Order.objects.get(pk=pk)
    order.status = 5
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_spare_from_order(request, order_id, spare_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(f"Заказа с таким id не существует")

    if not Spare.objects.filter(pk=spare_id).exists():
        return Response(f"Авиазапчасти с таким id не существует")

    order = Order.objects.get(pk=order_id)
    order.spares.remove(Spare.objects.get(pk=spare_id))
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


access_token_lifetime = settings.JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()


@api_view(["POST"])
def login(request):
    # Ensure email and passwords are posted properly
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Check credentials
    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "invalid credentials"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    # Create new access and refresh token
    access_token = create_access_token(user.id)

    # Add access token to redis for validating by other services
    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token,
    }
    cache.set(access_token, user_data, access_token_lifetime)

    # Create response object
    response = Response(user_data, status=status.HTTP_201_CREATED)
    # Set access token in cookie
    response.set_cookie('access_token', access_token, httponly=True, expires=access_token_lifetime)

    return response


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    user_data = {
        "user_id": user.id,
        "name": user.name,
        "email": user.email,
        "is_moderator": user.is_moderator,
        "access_token": access_token
    }

    cache.set(access_token, user_data, access_token_lifetime)

    message = {
        'message': 'User registered successfully',
        'user_id': user.id,
        "access_token": access_token
    }

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=access_token_lifetime)

    return response


@api_view(["POST"])
def check(request):
    access_token = get_access_token(request)

    if access_token is None:
        message = {"message": "Token is not found"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    if not cache.has_key(access_token):
        message = {"message": "Token is not valid"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    user_data = cache.get(access_token)

    return Response(user_data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    #  Check access token is in Redis
    if cache.has_key(access_token):
        # Delete access token from Redis
        cache.delete(access_token)

    # Create response object
    message = {"message": "Logged out successfully!"}
    response = Response(message, status=status.HTTP_200_OK)

    # Delete access token from cookie
    response.delete_cookie('access_token')

    return response