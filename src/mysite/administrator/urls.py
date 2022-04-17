from django.urls import path
from administrator import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('getname/', views.get_name, name='admin_get_name'),
    path('list_user/', views.ListUser.as_view(), name="admin_list_user"),
    path('designated_user/',views.DesignatedUser.as_view(),name='admin_designated_user')
]
