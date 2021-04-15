from django.urls import path
from .views import MovieView, CriticismReviewView

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movie_id>/review/", CriticismReviewView.as_view()),
]
