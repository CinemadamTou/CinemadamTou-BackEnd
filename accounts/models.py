from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie

def default_somemodel_dict():
    return {
        '28' : 0,
        '12' : 0,
        '16' : 0,
        '35' : 0,
        '80' : 0,
        '99' : 0,
        '18' : 0,
        '10751' : 0,
        '14' : 0,
        '36' : 0,
        '27' : 0,
        '10402' : 0,
        '9648' : 0,
        '10749' : 0,
        '878' : 0,
        '10770' : 0,
        '53' : 0,
        '10752' : 0,
        '37' : 0,
    }

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    like_movies = models.ManyToManyField(Movie, related_name='like_users')
    img = models.ImageField(upload_to='media/', blank=True)
    user_genre = models.JSONField(default=default_somemodel_dict)