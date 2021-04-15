from rest_framework import serializers
from .models import Movie, Classification, Genre, Comment, Criticism
from accounts.models import User
import ipdb


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class UserSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class UserCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "comment"]

    user = UserSetSerializer(read_only=True, many=True)


class CriticReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criticism
        fields = ["id", "critic", "stars", "review", "spoilers"]

    critic = UserSetSerializer(read_only=True, many=True)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "duration",
            "genres",
            "launch",
            "classification",
            "synopsis",
            "critic_reviews",
            "user_comments",
        ]

    def create(self, validated_data):
        classification = Classification.objects.get_or_create(
            age=validated_data["classification"]["age"]
        )[0]

        movie = Movie.objects.get_or_create(
            title=validated_data["title"],
            duration=validated_data["duration"],
            launch=validated_data["launch"],
            classification=classification,
            synopsis=validated_data["synopsis"],
        )[0]

        genres = validated_data["genres"]

        for genre in genres:
            genre_queryset = Genre.objects.get_or_create(name=genre["name"])[0]
            movie.genres.add(genre_queryset)

        return movie

    classification = ClassificationSerializer()
    genres = GenreSerializer(many=True)
    critic_reviews = CriticReviewsSerializer(many=True, read_only=True)
    user_comments = UserCommentsSerializer(many=True, read_only=True)
