from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'like_movies', 'like_reviews', 'followings', 'followers', 'img', 'user_genre')
        read_only_fields = ('id', 'like_movies', 'like_reviews', 'followings', 'followers',)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'like_movies', 'img', 'user_genre')
        read_only_fields = ('id',)