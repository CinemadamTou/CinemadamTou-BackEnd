from rest_framework import serializers
from .models import Review, Comment
from movies.models import Movie
from accounts.serializers import UserSerializer


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'movie_id', 'title','poster_path')


class ReviewSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'movie', 'like_users',)


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'review',)