from django.db import transaction
from django.utils import timezone
from rest_framework import exceptions, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from categories.models import Category
from media.models import Photo
from reservations.models import Reservation
from reservations.serializer import (
    CreateExpereinceReservation,
    PublicReservationSerializer,
)

from .models import Experience, Perk
from .serializer import (
    ExperienceDetailSerializer,
    ExperienceListSerailzer,
    PerkSerializer,
)


class Perks(APIView):

    def get(self, request):
        all_amenities = Perk.objects.all()
        serializer = PerkSerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(
                PerkSerializer(perk).data,
            )
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = PerkSerializer(
            perk,
            request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_serializer = serializer.save()
            return Response(
                PerkSerializer(updated_serializer).data,
            )
        else:
            return Response(serializer.error)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class Experiences(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = ExperienceListSerailzer(
            all_experiences,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category = request.data.get("category")
            if not category:
                raise exceptions.ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise exceptions.ParseError("Category kind should be Experience.")
            except Category.DoesNotExist:
                raise exceptions.ParseError("Category not found.")
            with transaction.atomic():
                experience = serializer.save(
                    host=request.user,
                    category=category,
                )
                perks = request.data.get("perks")
                if perks:
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
                else:
                    pass
                serializer = ExperienceDetailSerializer(experience)
                return Response(serializer.data)
        else:
            raise exceptions.ParseError


class ExperienceDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            exp = Experience.objects.get(pk=pk)
            return exp
        except Experience.DoesNotExist:
            raise exceptions.ParseError(f"Expereince id {pk} doesn't exist.")

    def get(self, request, pk):
        exp = self.get_object(pk)
        serializer = ExperienceDetailSerializer(exp)
        return Response(serializer.data)

    def post(self, request, pk):
        exp = self.get_object(pk)
        serializer = ExperienceDetailSerializer(
            exp,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            if request.data.get("host"):
                raise exceptions.ParseError(f"Expereince host is non changeable.")
            category_pk = request.data.get("category")
            if category_pk:
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise exceptions.ParseError(
                            "The category kind should be Expereinces"
                        )
                except Category.DoesNotExist:
                    raise exceptions.ParseError("Category not found")
            try:
                with transaction.atomic():
                    if category_pk:
                        updated_serializer = serializer.save(category=category)
                    else:
                        updated_serializer = serializer.save()
                    perks = request.data.get("perks")
                    if perks:
                        updated_serializer.perks.clear()
                        for perk_pk in perks:
                            try:
                                perk = Perk.objects.get(pk=perk_pk)
                            except:
                                raise exceptions.ParseError(
                                    f"non valid perk id {perk_pk}"
                                )
                            updated_serializer.perks.add(perk)

                    photos = request.data.get("photos")
                    if photos:
                        updated_serializer.photos.clear()
                        for photo_pk in photos:
                            photo = Photo.objects.get(pk=photo_pk)
                            if photo:
                                updated_serializer.photos.add(photo)
                            else:
                                raise exceptions.ParseError(
                                    f"non valid photo id {photo_pk}"
                                )

                    serializer = ExperienceDetailSerializer(updated_serializer)
            except:
                Response(serializer.errors)
            return Response(serializer.data)
        else:
            raise Response(serializer.errors)

    def delete(self, request, pk):
        exp = self.get_object(pk=pk)

        if exp.host != request.user:
            raise exceptions.PermissionDenied
        exp.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.ParseError("Experience dosen't exist.")

    def get(self, request, pk):
        experience = self.get_object(pk)
        perks = experience.perks.all()
        if perks:
            serializer = PerkSerializer(
                perks,
                many=True,
            )
            return Response(serializer.data)
        else:
            raise exceptions.NotFound


class ExperienceReservations(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise exceptions.ParseError(f"No Experience id {pk} found")

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localdate(timezone.now())
        reservations = experience.reservations.filter(experience_time__gte=now)
        if reservations:
            serializer = PublicReservationSerializer(
                reservations,
                many=True,
            )
            return Response(serializer.data)

    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExpereinceReservation(
            data=request.data,
            context={"duration": experience.duration},
        )
        if serializer.is_valid():
            kind = request.data.get("kind")
            if kind == Reservation.ReservationKindChoice.ROOM:
                raise exceptions.ParseError(
                    "The reservation kind should be Experience. Not Room."
                )
            reservation = serializer.save(
                user=request.user,
                experience=experience,
            )
            serializer = CreateExpereinceReservation(reservation)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceReservationDetail(APIView):
    # def get_experience(self, pk):
    #     try:
    #         return Experience.objects.get(pk=pk)
    #     except Experience.DoesNotExist:
    #         raise exceptions.NotFound

    def get_reservation(self, rv_pk):
        try:
            return Reservation.objects.get(pk=rv_pk)
        except Reservation.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk, rv_pk):
        # experience = self.get_experience(pk)
        reservation = self.get_reservation(rv_pk)
        serializer = PublicReservationSerializer(reservation)
        return Response(serializer.data)

    def delete(self, request, pk, rv_pk):
        reservation = self.get_reservation(rv_pk)
        reservation.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, pk, rv_pk):
        reservation = self.get_reservation(rv_pk)
        serializer = PublicReservationSerializer(
            reservation,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            reservation = serializer.save()
            serializer = PublicReservationSerializer(reservation)
            return Response(serializer.data)
        else:
            raise exceptions.ParseError("serializer not valid.")
