from django.shortcuts import get_object_or_404
import ipdb
from rest_framework import generics, filters
from .permissions import IsAdmin, IsCritic, IsAdminOrReadOnly
from rest_framework.authentication import TokenAuthentication
from .serializers import (
    MovieWithoutCritic,
    MovieSerializer,
    CriticReviewsSerializer,
    ReviewsSerializer,
)
from .models import Movie, Review
from accounts.models import User
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

class SearchForTitle(filters.SearchFilter):
    search_param = "title"


class MovieView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Movie.objects.all()
    serializer_class = MovieWithoutCritic
    filter_backends = [SearchForTitle]
    search_fields = ['title']
    

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

class ReviewView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Review.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCritic]
    serializer_class = CriticReviewsSerializer
    lookup_url_kwarg = "movie_id"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )
        
        movie = get_object_or_404(Movie, id=self.kwargs['movie_id']) 
        obj = get_object_or_404(queryset, movie=movie, critic=self.request.user)

        self.check_object_permissions(self.request, obj)

        return obj
    
class ListReviews(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin | IsCritic]
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff and not user.is_superuser:
            return Review.objects.filter(critic=user)
            
        return super().get_queryset()