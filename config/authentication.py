import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from users.models import User


class TrustAuthentication(BaseAuthentication):

    def authenticate(self, request):
        username = request.headers.get("Trust-Me")
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
            return (user, None)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(f"no user {username}")

        # return super().authenticate(request)
        return None


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Jwt")
        if not token:
            return None
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )
        pk = decoded.get("pk")
        if not pk:
            raise exceptions.AuthenticationFailed
        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")
