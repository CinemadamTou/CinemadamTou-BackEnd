from django.db import models
from django.conf import settings
from movies.models import Movie

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_reviews')
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk}. {self.title}'

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 댓글 좋아요 기능
    # like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')

    def __str__(self):
        return f'{self.pk}. {self.content}'