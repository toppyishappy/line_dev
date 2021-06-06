from django.contrib import admin
from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register', views.Register.as_view(), name='register'),
    path('', views.UserList.as_view(), name='user_list'),
    path('login', TokenObtainPairView.as_view()),
]