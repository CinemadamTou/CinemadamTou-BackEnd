from rest_framework import serializers
from django.contrib.auth import get_user_model
from movies.models import Genre

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'
            read_only_fields = ('genre_id', 'movies',)

    best_genres = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'like_movies', 'like_reviews', 'followings', 'followers', 'img', 'user_genre', 'user_phrase', 'reco_movies', 'user_intro', 'best_genres')
        read_only_fields = ('id', 'like_movies', 'like_reviews', 'followings', 'followers', 'img', 'user_genre', 'user_phrase', 'reco_movies', 'user_intro', 'best_genres')


class UserProfileSerializer(serializers.ModelSerializer):

    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'
            read_only_fields = ('genre_id', 'movies',)

    best_genres = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'like_movies', 'img', 'user_genre', 'user_phrase', 'reco_movies', 'user_intro', 'best_genres',)
        read_only_fields = ('id', 'img', 'user_genre', 'user_phrase', 'reco_movies', 'user_intro', 'best_genres')