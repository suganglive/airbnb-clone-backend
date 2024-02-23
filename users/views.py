# serializer.PrivateUserSeriazlier
from django.contrib.auth import authenticate, login, logout
from rest_framework import exceptions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.serializer import ReviewSerializer
from users.models import User
from users.serializer import TinyUserSerializer

# from . import serializer  # serializer.PrivateUserSeriazlier doesn't work.
from .serializer import PrivateUserSeriazlier


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PrivateUserSeriazlier(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serialzier = PrivateUserSeriazlier(
            user,
            data=request.data,
            partial=True,
        )
        if serialzier.is_valid():
            user = serialzier.save()
            serialzier = PrivateUserSeriazlier(user)
            return Response(serialzier.data)
        else:
            Response(serialzier.errors)


class Users(APIView):
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise exceptions.ParseError
        serializer = PrivateUserSeriazlier(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = PrivateUserSeriazlier(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class PublicUserProfile(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound
        serializer = PrivateUserSeriazlier(user)  # making PublicSerializer recommended
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise exceptions.ParseError
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserReviews(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.NotFound

        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size

        reviews = user.reviews.all()
        serializer = ReviewSerializer(
            reviews[start:end],
            many=True,
        )
        return Response(serializer.data)


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise exceptions.ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "welcome"})
        else:
            return Response({"error": "wrong password"})


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "bye"})
