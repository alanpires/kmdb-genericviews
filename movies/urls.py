from django.urls import path
from .views import (
    MovieView,
    MovieRetrieveDestroyView,
    CriticismReviewView,
    ListReviews
)

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movie_id>/", MovieRetrieveDestroyView.as_view()),
    path("movies/<int:movie_id>/review/", CriticismReviewView.as_view()),
    path("reviews/", ListReviews.as_view())
]
