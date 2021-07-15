from rest_framework import serializers
from .models import Movie, Criticism, Genre
from accounts.models import User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class UserSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class CriticReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criticism
        fields = ["id", "critic", "stars", "review", "spoilers"]

    critic = UserSetSerializer(read_only=True)
    stars = serializers.IntegerField(required=False, min_value=1, max_value=10)


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Criticism
        fields = ["id", "critic", "stars", "review", "spoilers", "movie"]

    critic = UserSetSerializer(read_only=True)
    stars = serializers.IntegerField(required=False, min_value=1, max_value=10)



class MovieWithoutCritic(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "duration",
            "genres",
            "premiere",
            "classification",
            "synopsis"
        ]

    def create(self, validated_data):
        movie = Movie.objects.get_or_create(
            title=validated_data["title"],
            duration=validated_data["duration"],
            premiere=validated_data["premiere"],
            classification=validated_data["classification"],
            synopsis=validated_data["synopsis"],
        )[0]

        genres = validated_data["genres"]

        for genre in genres:
            genre_created = Genre.objects.get_or_create(**genre)[0]
            movie.genres.add(genre_created)

        return movie

    genres = GenreSerializer(many=True)

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "duration",
            "genres",
            "premiere",
            "classification",
            "synopsis",
            "reviews",
        ]

    genres = GenreSerializer(many=True)
    reviews = CriticReviewsSerializer(many=True, read_only=True,)