from django.urls import include, path
from . import views

urlpatterns = [
    path('login', views.user_login, name='user_login'),
    path('profile', views.UserProfile.as_view()),
    path('solution', views.SolutionViewClass.as_view()),
    path('solution_like', views.solution_like),
    path('solution_report', views.solution_report),
    path('get_question', views.get_question, name='get_question'),
    path('wrong_que_book', views.wrong_que_bookClass.as_view()),
    path('record', views.recordClass.as_view()),
    path('notice', views.NoticeViewClass.as_view(), name='user_notice'),
    path('single_history', views.single_history),
    path('detail', views.detail),
    path('check_question', views.check_question),
    path('statistics', views.statistics),
    path('rank_que', views.rank_que),
    path('rank_sol', views.rank_sol),
]
