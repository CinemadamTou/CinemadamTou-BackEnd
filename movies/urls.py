from django.urls import path
from . import views

urlpatterns = [
    # path('research/', views.research),
    path('tindermovie/', views.tindermovie),
    path('genre/', views.genre_list),
    path('genre/<int:genre_pk>/movies/', views.genre_movies),
    path('new/', views.new),
    path('create/',views.create),
    path('', views.movie_list),
    path('search/', views.search),
    path('<int:movie_pk>/', views.movie_detail),
    path('<int:movie_pk>/recommend/', views.movie_recommend),
    path('<int:movie_pk>/actors/', views.movie_actors),
    path('<int:movie_pk>/images/', views.movie_images),
    path('<int:movie_pk>/videos/', views.movie_videos),
    path('<int:movie_pk>/reviews/', views.movie_review_create),
    path('<int:movie_pk>/comments/', views.movie_comment_list_create),
    path('<int:movie_pk>/comments/<int:movie_comment_pk>/', views.movie_comment_update_delete),
    path('<int:movie_pk>/like/', views.movie_like),
    path('<int:movie_pk>/vote/', views.movie_vote),
]