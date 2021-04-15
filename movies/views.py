from django.shortcuts import render
from rest_framework import generics
from .permissions import IsAdmin, IsCritic
from rest_framework.authentication import TokenAuthentication
from .serializers import MovieSerializer, CriticReviewsSerializer
from .models import Movie, Criticism
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


class MultipleFieldLookupMixin:
    def get_queryset(self):
        queryset = self.queryset
        lookup_filter = {}
        for lookup_field in self.lookup_fields:
            if self.request.data.get(lookup_field):

                lookup_filter[f"{lookup_field}__icontains"] = self.request.data.get(
                    lookup_field
                )

        queryset = queryset.filter(**lookup_filter)
        return queryset


class MovieView(MultipleFieldLookupMixin, generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_fields = ["title"]


class CriticismReviewView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCritic]
    serializer_class = CriticReviewsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movie = Movie.objects.get(id=kwargs["movie_id"])
        critic = Criticism.objects.filter(movie=movie, critic=request.user)

        if len(critic) == 0:
            critic = Criticism.objects.create(
                stars=request.data["stars"],
                review=request.data["review"],
                spoilers=request.data["spoilers"],
            )
            critic.critic.add(request.user)

            movie = Movie.objects.get(id=kwargs["movie_id"])
            critic.movie_set.add(movie)

            serializer = CriticReviewsSerializer(critic)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

        else:
            return Response(
                {"detail": "You already made this review."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )