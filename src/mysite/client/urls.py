from django.urls import include, path
from . import views

urlpatterns = [
    path('login', views.user_login, name='user_login')

]
