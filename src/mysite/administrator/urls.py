from django.urls import path
from administrator import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('getname/', views.get_name, name='admin_get_name')
]
