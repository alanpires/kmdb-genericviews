import ipdb
from rest_framework import generics
from .permissions import IsAdmin, IsCritic, IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication
from .serializers import (
    MovieWithoutCritic,
    MovieSerializer,
    CriticReviewsSerializer,
    ReviewsSerializer,
)
from .models import Movie, Criticism
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist


class MovieView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Movie.objects.all()
    serializer_class = MovieWithoutCritic

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if request.query_params.get('title', None):
            queryset = queryset.filter(title__icontains=request.query_params.get('title', None))
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class MovieRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_url_kwarg = "movie_id"
    
    def get_serializer(self, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.method != 'PUT':
            return super().get_serializer(*args, **kwargs)
        serializer_class = MovieWithoutCritic
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

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
                    critic=request.user,
                    movie=movie,
                )

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
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND,
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
        return Response(serializer.data)
    
class ListReviews(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin | IsCritic]
    queryset = Criticism.objects.all()
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff and not user.is_superuser:
            return Criticism.objects.filter(critic=user)
            
        return super().get_queryset()