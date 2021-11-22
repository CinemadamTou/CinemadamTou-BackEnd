from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Review, Comment
from movies.models import Movie

from .serializers import ReviewSerializer, CommentSerializer


# 전체 게시글 갯수 조회
@api_view(['GET'])
def review_cnt(request):
    reviews = get_list_or_404(Review)
    review_cnt = len(reviews)
    data ={
        'review_cnt': review_cnt
    }
    return Response(data)

# page 게시글 조회 (paginator)
@api_view(['GET'])
def review_list(request):
    reviews = get_list_or_404(Review)
    paginator = Paginator(reviews, 10)
    page_num = request.GET.get("page")
    page_obj = paginator.get_page(page_num)
    serializer = ReviewSerializer(page_obj, many=True)
    return Response(serializer.data)

# 게시글 상세, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_update_delete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    # 게시글 상세 조회
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    # 게시글 수정
    elif request.method == 'PUT':
        if review.user == request.user:
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        return Response(status=401)

    # 게시글 삭제
    elif request.method == 'DELETE':
        if review.user == request.user:
            review.delete()
            return Response({ 'id': review_pk }, status=status.HTTP_204_NO_CONTENT)
        return Response(status=401)

# 댓글 조회, 생성
@api_view(['GET', 'POST'])
def comment_list_create(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)

    # 댓글 조회
    if request.method == 'GET':
        comments = review.review_comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # 댓글 생성
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, review=review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# 댓글 수정, 삭제
@api_view(['PUT', 'DELETE'])
def comment_update_delete(request, review_pk, comment_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    # 댓글 수정
    if request.method == 'PUT':
        if comment.user == request.user:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        return Response(status=401)
        
    # 댓글 삭제
    elif request.method == 'DELETE':
        if comment.user == request.user:
            comment.delete()
            return Response({'id' : comment_pk}, status=status.HTTP_204_NO_CONTENT)
        return Response(status=401)

# 게시글 좋아요
@api_view(['POST'])
def review_like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    # if request.user.is_authenticated:
    user = request.user
    if review.user != user:
        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)
            is_like = False
        else:
            review.like_users.add(user)
            is_like = True
        data = {
            'is_like': is_like,
        }
        return Response(data)
    return Response(status=401)