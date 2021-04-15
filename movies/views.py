from django.shortcuts import render
from rest_framework import generics
from .permissions import IsAdmin, IsCritic, IsUser
from rest_framework.authentication import TokenAuthentication
from .serializers import MovieSerializer, CriticReviewsSerializer
from .models import Movie, Criticism, Comment
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


class CriticismReviewView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Movie.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCritic]
    serializer_class = CriticReviewsSerializer
    lookup_url_kwarg = "movie_id"

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
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

        except ObjectDoesNotExist:
            return Response(
                {"detail": "invalid_movie_id"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        movie = Movie.objects.get(id=kwargs["movie_id"])
        try:
            critic = Criticism.objects.get(movie=movie, critic=request.user)

        except ObjectDoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        critic.stars = request.data["stars"]
        critic.review = request.data["review"]
        critic.spoilers = request.data["spoilers"]
        critic.save()
        serializer = CriticReviewsSerializer(critic)
        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)


# class CommentReviewView(generics.CreateAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsUser]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         comment = Comment.objects.create(comment=request.data["comment"])

#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             serializer.data, status=status.HTTP_201_CREATED, headers=headers
#         )
