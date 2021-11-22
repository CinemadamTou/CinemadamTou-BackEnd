from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer, UserProfileSerializer
from movies.models import Movie
from movies.serializers import MovieSerializer

# 회원가입
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    # 1-1. Client에서 온 데이터를 받아서
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')

    # 1-2. 패스워드 일치 여부 체크
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 2. UserSerializer를 통해 데이터 직렬화
    serializer = UserSerializer(data=request.data)

    # 3. validation (password도 같이 직렬화 작업 진행)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        # 4. 비밀번호 해싱
        user.set_password(request.data.get('password'))
        # user.set_password(password)
        user.save()
        # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않음(write_only)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 사용자 이름 불러오기
@api_view(['GET'])
def get_username(request):
    user = get_object_or_404(get_user_model(), username=request.user.username)
    serializer = UserSerializer(user)
    return Response(serializer.data)

# 사용자 프로필
@api_view(['GET'])
def profile(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    data = []
    serializer = UserProfileSerializer(user)
    data.append(serializer.data)
    movies = user.like_movies.all()
    serializer = MovieSerializer(movies, many=True)
    data.append(serializer.data)
    return Response(data)

# 사용자 팔로우
@api_view(['POST'])
def user_follow(request, user_pk):
    person = get_object_or_404(get_user_model(), pk=user_pk)
    user = request.user
    if person != user:
        if person.followers.filter(pk=user.pk).exists():
            person.followers.remove(user)
            is_follow = False
        else:
            person.followers.add(user)
            is_follow = True
        data = {
            "is_follow": is_follow,
        }
        return Response(data)
    return Response(status=401)