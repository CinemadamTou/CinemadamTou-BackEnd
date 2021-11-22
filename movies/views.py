from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from community.serializers import ReviewSerializer
from .models import Movie, MovieComment, Genre, MovieScore

from .serializers import MovieSerializer, MovieCommentSerializer, GenreSerializer, MovieScoreSerializer, MovieTinderSerializer
from community.serializers import ReviewSerializer

from datetime import datetime
from django.utils.dateformat import DateFormat
from django.contrib.auth import get_user_model
import random

# @api_view(['POST'])
# def research(request):
#     user = get_object_or_404(get_user_model(), username=request.user)
#     movies = reqeust.data
#     for movie in movies:
#         url = f'https://api.themoviedb.org/3/movie/{movie.movie_id}/recommendations?api_key=41c1e2697868f05090a2fb5fd80bad45&language=ko-KR&page=1'
#         res = requests.get(url)
#         recomovies = res.json().get('results')
#         movies = get_list_or_404(Movie)
#         for recomovie in recomovies:
#             if Movie.objects.filter(movie_id=recomovie['id']).exists():
#                 td_movie = get_object_or_404(Movie, movie_id=recomovie['id'])
#                 recogenres = td_movie.genres
#                 for recogenre in recogenres:
#                     user.user_genres[str(recogenre)] += 1
#     return Response(status=status.HTTP_201_CREATED)

# 영화 목록 조회
@api_view(['GET'])
def movie_list(request):
    # movies = get_list_or_404(Movie)
    movies = Movie.objects.order_by('?')[:60]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

# 영화 상세 정보
@api_view(['GET'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)

# 영화 게시글 작성
@api_view(['POST'])
def movie_review_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ReviewSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 영화 댓글 조회, 작성
@api_view(['GET', 'POST'])
def movie_comment_list_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    # 영화 댓글 조회
    if request.method == 'GET':
        movie_comments = movie.movie_comments.all()
        serializer = MovieCommentSerializer(movie_comments, many=True)
        return Response(serializer.data)

    # 영화 댓글 작성
    elif request.method == 'POST':
        serializer = MovieCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 영화 댓글 수정, 삭제
@api_view(['PUT', 'DELETE'])
def movie_comment_update_delete(request, movie_pk, movie_comment_pk):
    comment = get_object_or_404(MovieComment, pk=movie_comment_pk)

    # 영화 댓글 수정
    if request.method == 'PUT':
        if comment.user == request.user:
            serializer = MovieCommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        return Response(status=401)

    # 영화 댓글 삭제
    elif request.method == 'DELETE':
        if comment.user == request.user:
            comment.delete()
            return Response({ 'id': movie_comment_pk }, status=status.HTTP_204_NO_CONTENT)
        return Response(status=401)

# 영화 평점 조회, 추가, 수정
@api_view(['GET', 'POST', 'PUT'])
def movie_vote(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user

    # 영화 평점 조회
    if request.method == 'GET':
        if movie.voted_users:
            if movie.voted_users.filter(pk=user.pk).exists():
                moviescore = get_object_or_404(MovieScore, user=user, movie=movie)
                serializer = MovieScoreSerializer(moviescore)
                return Response(serializer.data)
            else:
                data = {
                    'score': 0,
                }
                return Response(data)
        return Response(status=401)

    # 영화 평점 추가
    elif request.method == 'POST':
        if movie.voted_users and movie.voted_users.filter(pk=user.pk).exists():
            return Response(status=401)
        else:
            serializer = MovieScoreSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, movie=movie)
                movie.voted_users.add(user)
    # 영화 평점 수정
    elif request.method == 'PUT':
        if movie.voted_users and movie.voted_users.filter(pk=user.pk).exists():
            moviescore = get_object_or_404(MovieScore, user=user, movie=movie)
            serializer = MovieScoreSerializer(moviescore, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        else:
            return Response(status=401)

        # 영화 평점 데이터에 반영
        moviescores = MovieScore.objects.all().filter(movie=movie)
        total = 0
        for movescore in moviescores:
            total += movescore.score
        movie.score = ((movie.origin_score * 10) + total) / (len(moviescores) + 10)
        movie.score_count = len(moviescores) + 10
        movie.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 영화 좋아요
@api_view(['POST'])
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    # if request.user.is_authenticated:
    user = request.user
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        isLike = False
    else:
        movie.like_users.add(user)
        isLike = True
    data = {
        'isLike': isLike,
    }
    return Response(data)

# 영화 검색
@api_view(['POST'])
def search(request):
    keyword = request.data.get('inputData')
    movies = Movie.objects.filter(Q(title__contains=keyword) | Q(overview__contains=keyword)).distinct()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

# 관련 영화 추천
@api_view(['GET'])
def movie_recommend(request, movie_pk):
    data = []
    movie = get_object_or_404(Movie, pk=movie_pk)
    url = f'https://api.themoviedb.org/3/movie/{movie.movie_id}/recommendations?api_key=41c1e2697868f05090a2fb5fd80bad45&language=ko-KR&page=1'
    res = requests.get(url)
    recomovies = res.json().get('results')
    movies = get_list_or_404(Movie)
    for recomovie in recomovies:
        if Movie.objects.filter(movie_id=recomovie['id']).exists():
            movie = get_object_or_404(Movie, movie_id=recomovie['id'])
            serializer = MovieSerializer(movie)
            data.append(serializer.data)
    # 랜덤한 4개의 숫자 활용해서 랜덤 추천 구현
    random_nums = random.sample(range(len(data)), min(4, len(data)))
    random_data = []
    for num in random_nums:
        random_data.append(data[num])
    return Response(random_data)

# 개봉 예정 영화
@api_view(['GET'])
def new(request):
    today = DateFormat(datetime.now()).format('Y-m-d')
    new_movies = Movie.objects.all().filter(release_date__gt = f'{today}').order_by('?')
    serializer = MovieSerializer(new_movies, many=True)
    return Response(serializer.data)

# 단일 장르별 영화
# *차후 복수 장르별 영화 구현*
@api_view(['GET'])
def genre_movies(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    movies = genre.movies.all().order_by('?')
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

# 영화 출현 배우 목록
@api_view(['GET'])
def movie_actors(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    url = f'https://api.themoviedb.org/3/movie/{movie.movie_id}/credits?api_key=41c1e2697868f05090a2fb5fd80bad45&language=ko-KR'
    res = requests.get(url)
    actors = res.json().get('cast')[:4]
    return Response(actors)

# 영화 관련 이미지
@api_view(['GET'])
def movie_images(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    url = f'https://api.themoviedb.org/3/movie/{movie.movie_id}/images?api_key=41c1e2697868f05090a2fb5fd80bad45'
    res = requests.get(url)
    images = res.json().get('backdrops')[:4]
    return Response(images)

# 영화 관련 영상
@api_view(['GET'])
def movie_videos(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    url = f'https://api.themoviedb.org/3/movie/{movie.movie_id}/videos?api_key=41c1e2697868f05090a2fb5fd80bad45&language=ko-KR'
    res = requests.get(url)
    videos = res.json().get('results')
    url = f'https://api.themoviedb.org/3/movie/{movie.movie_id}/videos?api_key=41c1e2697868f05090a2fb5fd80bad45&language=en-US'
    res = requests.get(url)
    videos.extend(res.json().get('results'))
    return Response(videos[:4])

# 장르 리스트
@api_view(['GET'])
def genre_list(request):
    genres = get_list_or_404(Genre)
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

# 틴더로 보낼 영화 리스트
@api_view(['GET'])
def tindermovie(request):
    movies = Movie.objects.order_by('?')[:30]
    serializer = MovieTinderSerializer(movies, many=True)
    return Response(serializer.data)

# DB 구성 페이지
@api_view(['GET'])
def create(request):
    API_KEY = "41c1e2697868f05090a2fb5fd80bad45"

    url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={API_KEY}&language=ko-KR'
    movie_response = requests.get(url).json()

    for tmdb_movie in movie_response['genres']:
        genre = Genre()
        genre.genre_id = tmdb_movie['id']
        genre.name = tmdb_movie['name']
        genre.save()

    for i in range(1, 16):
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=ko-KR&page={i}&region=KR'
        movie_response = requests.get(url).json()
        for tmdb_movie in movie_response['results']:
            movie = Movie()
            movie.title = tmdb_movie['title']
            movie.movie_id = tmdb_movie['id']
            movie.adult = tmdb_movie['adult']
            movie.overview = tmdb_movie['overview']
            movie.score = tmdb_movie['vote_average']
            movie.score_count = 10
            movie.origin_score = movie.score
            movie.release_date = tmdb_movie['release_date']
            movie.poster_path = tmdb_movie['poster_path']
            movie.save()

    movies = Movie.objects.all()
    genres = Genre.objects.all()
    for move in movies:
        url = f'https://api.themoviedb.org/3/movie/{move.movie_id}?api_key=41c1e2697868f05090a2fb5fd80bad45&language=ko-KR'
        movie_response = requests.get(url).json()
        for tmdb in movie_response['genres']:
            for gen in genres:
                if tmdb['name'] == gen.name:
                    gen.movies.add(move.id)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)