from django.conf import settings
from rest_framework.permissions import BasePermission

from .jwt_helper import get_access_token, get_jwt_payload
from .models import CustomUser


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        token = get_access_token(request)

        if token is None:
            return False

        try:
            payload = get_jwt_payload(token)
        except Exception as e:
            return False

        try:
            user = CustomUser.objects.get(pk=payload["user_id"])
        except Exception as e:
            return False

        return user.is_active


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        token = get_access_token(request)

        if token is None:
            return False

        # Ensure token is valid
        try:
            payload = get_jwt_payload(token)
        except Exception as e:
            return False

        # Ensure user exists
        try:
            user = CustomUser.objects.get(pk=payload["user_id"])
        except Exception as e:
            return False

        return user.is_moderator


class IsRemoteWebService(BasePermission):
    def has_permission(self, request, view):
        access_token = request.data.get("access_token", "")
        return access_token == settings.REMOTE_WEB_SERVICE_AUTH_TOKEN