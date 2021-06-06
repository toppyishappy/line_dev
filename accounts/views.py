from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from accounts.serializer import RegisterSerializer, UserListSerializer
from accounts.models import User

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import permissions
# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class Register(CreateAPIView):
    serializer_class = RegisterSerializer


class UserList(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserListSerializer