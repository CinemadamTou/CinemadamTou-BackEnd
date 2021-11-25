from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('profile/<int:user_pk>/', views.profile),
    path('profile/image/', views.upload_profile_image),
    path('profile/phrase/', views.set_user_phrase),
    path('profile/intro/', views.change_user_intro),
    path('profile/<int:user_pk>/follow/', views.user_follow),
    path('signup/', views.signup),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('username/', views.get_username),
]