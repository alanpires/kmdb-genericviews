from rest_framework import serializers
from .models import Movie, Review, Genre
from accounts.models import User
from .exceptions import ReviewException
from django.shortcuts import get_object_or_404
import ipdb

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
        model = Review
        fields = ["id", "critic", "stars", "review", "spoilers"]

    critic = UserSetSerializer(read_only=True)
    stars = serializers.IntegerField(required=False, min_value=1, max_value=10)
    
    def validate(self, attrs):
        if self.context['request'].method == 'POST':
            movie = get_object_or_404(Movie, id=self.context['view'].kwargs['movie_id'])
            review = Review.objects.filter(movie=movie, critic=self.context['request'].user).exists()
            if review:
                raise ReviewException
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data['critic_id'] = self.context['request'].user.id
        validated_data['movie_id'] = self.context['view'].kwargs['movie_id']
        return super().create(validated_data)


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "critic", "stars", "review", "spoilers", "movie"]

    critic = UserSetSerializer(read_only=True)
    stars = serializers.IntegerField(required=False, min_value=1, max_value=10)



class MovieWithoutCritic(serializers.ModelSerializer):
    
    genres = GenreSerializer(many=True)
    
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
    
    def update(self, instance, validated_data):
        instance.title =validated_data.get("title")
        instance.duration=validated_data.get("duration")
        instance.premiere=validated_data.get("premiere")
        instance.classification=validated_data.get("classification")
        instance.synopsis=validated_data.get("synopsis")

        genres = validated_data.get("genres")

        instance.save()
        
        for genre in genres:
            genre_created = Genre.objects.get_or_create(**genre)[0]
            instance.genres.add(genre_created)

        return instance

    

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