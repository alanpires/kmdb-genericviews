from django.urls import path
from .views import (
    MovieView,
    MovieRetrieveDestroyView,
    ReviewView,
    ListReviews
)

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movie_id>/", MovieRetrieveDestroyView.as_view()),
    path("movies/<int:movie_id>/review/", ReviewView.as_view()),
    path("reviews/", ListReviews.as_view())
]
