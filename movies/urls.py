from django.urls import path
from .views import MovieView, MovieRetrieveView, CriticismReviewView, CommentReviewView

urlpatterns = [
    path("movies/", MovieView.as_view()),
    path("movies/<int:movie_id>/", MovieRetrieveView.as_view()),
    path("movies/<int:movie_id>/review/", CriticismReviewView.as_view()),
    path("movies/<int:movie_id>/comments/", CommentReviewView.as_view()),
]
