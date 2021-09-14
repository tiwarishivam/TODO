import logging
from django.shortcuts import render
from django.contrib.auth.models import AbstractUser, PermissionsMixin, User

from rest_framework import generics, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction

from django.contrib.auth import authenticate, get_user_model, login

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Login(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({
                'message': 'login successfull'
            }, status=200)

        return Response({
            'message': 'login credentials invalid'
        }, status=400)


class GetUser(APIView):
    perissions = (IsAuthenticated)

    def get(self, request):
        user = request.user

        return Response({
            'user': user.username
        }, status=200)
