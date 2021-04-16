from django.db import models
from accounts.models import User


class Genre(models.Model):
    name = models.CharField(max_length=255)


class Movie(models.Model):
    title = models.TextField()
    duration = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    launch = models.DateField(null=True, blank=True)
    classification = models.IntegerField(null=True, blank=True)
    synopsis = models.TextField(null=True, blank=True)


class Criticism(models.Model):
    critic = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)