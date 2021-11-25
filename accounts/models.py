from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie, Genre

def default_somemodel_dict():
    return {
        '28' : 0,
        '12' : 0,
        '16' : 0,
        '35' : 0,
        '80' : 0,
        '18' : 0,
        '10751' : 0,
        '14' : 0,
        '27' : 0,
        '9648' : 0,
        '10749' : 0,
        '878' : 0,
        '53' : 0,
    }

def users_image_path(instance, filename):
    return f'user_{instance.pk}/{filename}'

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    like_movies = models.ManyToManyField(Movie, related_name='like_users')
    reco_movies = models.ManyToManyField(Movie, related_name='reco_users')
    img = models.ImageField(upload_to=users_image_path, default='media/profileimg.jpg')
    user_genre = models.JSONField(default=default_somemodel_dict)
    user_phrase = models.CharField(max_length=100, blank=True)
    user_intro = models.CharField(max_length=50, blank=True)
    best_genres = models.ManyToManyField(Genre, related_name='best_users')