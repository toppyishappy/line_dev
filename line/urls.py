from django.contrib import admin
from django.urls import path
from line import views

urlpatterns = [
    path('callback/', views.Callback.as_view(), name='callback'),
]