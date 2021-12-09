from rest_framework import serializers
from .models import Movie, Review, Genre
from accounts.models import User
from .exceptions import ReviewException
from django.shortcuts import get_object_or_404

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
        exclude = ['movie']

    critic = UserSetSerializer(read_only=True)
    stars = serializers.IntegerField(min_value=1, max_value=10)
    
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
        fields = '__all__'

    critic = UserSetSerializer(read_only=True)


class MovieWithoutCritic(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    
    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, validated_data):
        genres = validated_data.pop("genres")
        
        movie = Movie.objects.get_or_create(**validated_data)[0]

        for genre in genres:
            genre_created = Genre.objects.get_or_create(**genre)[0]
            movie.genres.add(genre_created)

        return movie
    
    def update(self, instance, validated_data):
        genres = validated_data.pop("genres")
        
        genres_list = []
        
        for genre in genres:
            genre_created = Genre.objects.get_or_create(**genre)[0]
            genres_list.append(genre_created)
        
        instance.genres.set(genres_list)

        return super().update(instance, validated_data)

    

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    genres = GenreSerializer(many=True)
    reviews = CriticReviewsSerializer(many=True, read_only=True,)