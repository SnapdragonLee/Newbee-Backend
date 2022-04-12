from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from utils.response import drf_response
from utils.auth_decorators import admin_logged


# Create your views here.
@api_view(['POST'])
def admin_login(request):
    username = request.data['name']
    password = request.data['pwd']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return drf_response(0)
    else:
        return drf_response(1)


@admin_logged
@api_view(['DELETE'])
def admin_logout(request):
    logout(request)
    return drf_response(0)
