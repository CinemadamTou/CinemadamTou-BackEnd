from rest_framework import serializers
from .models import Movie, MovieComment, Genre, MovieScore
from accounts.serializers import UserSerializer


class MovieSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

class MovieCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MovieComment
        fields = '__all__'
        read_only_fields = ('user', 'movie',)

class MovieScoreSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = MovieScore
        fields = '__all__'
        read_only_fields = ('user', 'movie',)

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

class MovieTinderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'movie_id','title', 'poster_path', 'genres',)