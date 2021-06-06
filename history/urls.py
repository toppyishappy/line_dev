from django.contrib import admin
from django.urls import path
from history import views

urlpatterns = [
    path('', views.ReserveList.as_view(), name='reserve_list'),
    path('my', views.BookerReserved.as_view(), name='reserve_list'),
]