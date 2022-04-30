from django.urls import include, path
from . import views

urlpatterns = [
    path('login', views.user_login, name='user_login'),
    path('solution', views.SolutionViewClass.as_view()),
    path('solution_like', views.solution_like),
    path('solution_report', views.solution_report)
]
