from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import (
    NotAuthenticated,
    NotFound,
    ParseError,
    PermissionDenied,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from categories.models import Category
from media.serializer import PhotoSerializer
from reservations.models import Reservation
from reservations.serializer import (
    CreateRoomReservationSerializer,
    PublicReservationSerializer,
)
from reviews.serializer import ReviewSerializer

from .models import Amenity, Room
from .serializer import (
    AmenitiySerializer,
    ReviewSerializer,
    RoomDetailSerializer,
    RoomListSerializer,
)


class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitiySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitiySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitiySerializer(amenity).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class AmenitiyDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitiySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitiySerializer(
            amenity,
            request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_serializer = serializer.save()
            return Response(
                AmenitiySerializer(updated_serializer).data,
            )
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Rooms(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):

        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request):

        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            category = request.data.get("category")
            if not category:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category)
                if category.kind == Category.CategoryKindChoices.EXPERIENCE:
                    raise ParseError("Category kind should be rooms.")
            except Category.DoesNotExist:
                raise ParseError("Category not found.")
            try:
                with transaction.atomic():
                    room = serializer.save(
                        owner=request.user,
                        category=category,
                    )
                    amenities = request.data.get("amenities")
                    # work with manytomany field. first make room and add amenities later.
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(room)
                    return Response(serializer.data)
            except Exception:
                raise ParseError("Amenity not found.")

        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class RoomDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk=pk)
        serializer = RoomDetailSerializer(
            room,
            context={"request": request},
        )
        return Response(serializer.data)

    def delete(self, request, pk):
        room = self.get_object(pk=pk)

        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        room = self.get_object(pk=pk)

        if room.owner != request.user:
            raise PermissionDenied
        serializer = RoomDetailSerializer(
            room,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be rooms")
                except Category.DoesNotExist:
                    raise ParseError("Category not found")

            try:
                with transaction.atomic():
                    if category_pk:
                        updated_serializer = serializer.save(category=category)
                    else:
                        updated_serializer = serializer.save()

                    amenities = request.data.get("amenities")
                    if amenities:
                        room.amenities.clear()
                        # print(amenities)
                        for amenity_pk in amenities:
                            # print(amenity_pk)
                            amenity = Amenity.objects.get(pk=amenity_pk)

                            updated_serializer.amenities.add(amenity)

                return Response(
                    RoomDetailSerializer(
                        updated_serializer,
                        context={"request": request},
                    ).data
                )
            except Exception:
                raise ParseError("somethings wrong.")

        else:
            return Response(serializer.errors)


class RoomReviews(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        serializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(pk=pk),
            )
        serializer = ReviewSerializer(review)
        return Response(serializer.data)


class RoomAmenities(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1
        page_size = 3
        start = (page - 1) * page_size
        end = start + page_size

        room = self.get_object(pk)
        serializer = AmenitiySerializer(
            room.amenities.all()[start:end],
            many=True,
        )
        return Response(serializer.data)


class RoomPhotos(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk=pk)
        if request.user != room.owner:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class RoomReservations(APIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]  # get is free but else are needed to authenticated

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, requset, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()
        reservations = Reservation.objects.filter(
            room=room,
            kind=Reservation.ReservationKindChoice.ROOM,
            check_in__gt=now,
        )
        serializer = PublicReservationSerializer(
            reservations,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save(
                room=room,
                user=request.user,
                kind=Reservation.ReservationKindChoice.ROOM,
            )
            serializer = PublicReservationSerializer(reservation)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
