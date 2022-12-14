from django.db import models
from accounts.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255)


class Movie(models.Model):
    title = models.TextField()
    duration = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    premiere = models.DateField(null=True, blank=True)
    classification = models.IntegerField(null=True, blank=True)
    synopsis = models.TextField(null=True, blank=True)


class Review(models.Model):
    critic = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')
