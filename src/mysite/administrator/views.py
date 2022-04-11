from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.
@api_view(['POST'])
def admin_login(request):
    if request.user.is_authenticated:
        return Response(data={"ret": '0'}, status=200)

    username = request.data['name']
    password = request.data['pwd']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return Response(data={"ret": '0'}, status=200)
    else:
        return Response(data={"ret": '1'}, status=200)


@api_view(['DELETE'])
def admin_logout(request):
    logout(request)
    return Response(data={"ret": '0'}, status=200)
