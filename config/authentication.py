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
