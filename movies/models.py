from django.db import models
from django.conf import settings

class Movie(models.Model):
    movie_id = models.IntegerField()
    adult = models.BooleanField()
    title = models.CharField(max_length=100)
    overview = models.TextField()
    score = models.FloatField()
    score_count = models.IntegerField()
    origin_score = models.FloatField()
    voted_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='vote_movies')
    release_date = models.CharField(max_length=50)
    poster_path = models.TextField()

    def __str__(self):
        return f'{self.pk}. {self.title}'

class MovieScore(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movie_score')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_score')

class MovieComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_comments')
    content = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.pk}. {self.content}'

class Genre(models.Model):
    movies = models.ManyToManyField(Movie, related_name='genres')
    genre_id = models.IntegerField()
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.pk}. {self.name}'