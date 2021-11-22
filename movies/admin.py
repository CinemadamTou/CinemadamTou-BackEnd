from django.contrib import admin
from .models import Movie, MovieComment, Genre, MovieScore

admin.site.register(Movie)
admin.site.register(MovieComment)
admin.site.register(Genre)
admin.site.register(MovieScore)