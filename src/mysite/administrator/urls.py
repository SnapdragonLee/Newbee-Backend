from django.urls import path
from administrator import views

urlpatterns = [
    path('login', views.admin_login, name='admin_login'),
    path('logout', views.admin_logout, name='admin_logout'),
    path('getname', views.get_name, name='admin_get_name'),
    path('list_user', views.ListUser.as_view(), name="admin_list_user"),
    path('designated_user', views.DesignatedUser.as_view(), name='admin_designated_user'),
    path('list_question', views.ListQuestion.as_view(), name='admin_list_question'),
    path('designated_question', views.DesignatedQuestion.as_view(), name='admin_designated_question'),
    path('solution', views.ListSolution.as_view(), name='admin_solution'),
    path('has_bad_solution', views.has_bad_solution, name='admin_has_bad_solution'),
    path('notice', views.NoticeViewClass.as_view(), name='admin_notice'),
    path('op_record', views.get_operation_record, name='admin_op_record'),
    path('graph', views.get_graph_data, name='admin_get_graph_data'),
]
