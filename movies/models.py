from django.db import models
from accounts.models import User


class Criticism(models.Model):
    critic = models.ManyToManyField(User)
    stars = models.IntegerField()
    review = models.TextField()
    spoilers = models.BooleanField()


class Comment(models.Model):
    user = models.ManyToManyField(User)
    comment = models.TextField()


class Classification(models.Model):
    age = models.IntegerField()


class Genre(models.Model):
    name = models.TextField()


class Movie(models.Model):
    title = models.TextField()
    duration = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)
    launch = models.DateField(null=True, blank=True)
    classification = models.ForeignKey(
        Classification, on_delete=models.CASCADE, null=True, blank=True
    )
    synopsis = models.TextField(null=True, blank=True)
    critic_reviews = models.ManyToManyField(Criticism)
    user_comments = models.ManyToManyField(Comment)