from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from utils.response import wrap_response_data
from utils.auth_decorators import admin_logged
from django.http import JsonResponse
from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from client import models as client_models
from . import models as admin_models
from client.serializers import ListUserSerializer
from .serializers import ListQuestionSerializer, DesignatedQuestionSerializer, SubQuestionSerializer
from django.core import serializers
from django.utils.decorators import method_decorator
import json
from utils.defines import *
from django.core.exceptions import ValidationError


# Create your views here.
def admin_login(request):
    username = request.POST['name']
    password = request.POST['pwd']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse(data=wrap_response_data(0))

    else:
        return JsonResponse(data=wrap_response_data(3, "用户名或密码错误"))


@admin_logged
def admin_logout(request):
    logout(request)
    return JsonResponse(data=wrap_response_data(0))


@admin_logged
def get_name(request):
    data = {'name': request.user.username}
    return JsonResponse(data=wrap_response_data(0, **data))


def get_user_list(page_num, page_size, query_set):
    paginator = Paginator(query_set, page_size)
    user_list = paginator.get_page(page_num).object_list
    total = query_set.count()
    serializer = ListUserSerializer(user_list, many=True)
    return {'list': json.loads(json.dumps(serializer.data)),
            'total': total}


class ListUser(View):
    @method_decorator(admin_logged)
    def get(self, request):
        page_number = request.GET['pagenumber']
        page_size = request.GET['pagesize']
        query_set = client_models.WXUser.objects.all().order_by("user_name")
        data = get_user_list(page_number, page_size, query_set)
        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(admin_logged)
    def delete(self, request):
        id_list = request.GET.getlist('userid')  # 根据赵佬的提醒获取DELETE的参数也得用GET
        user_list = []
        try:
            for user_id in id_list:
                user_list.append(client_models.WXUser.objects.get(id=user_id))
        except Exception:
            return JsonResponse(data=wrap_response_data(3, '部分或全部用户id不存在，未执行任何删除操作'))

        for user in user_list:
            user.delete()

        return JsonResponse(data=wrap_response_data(0))


class DesignatedUser(View):
    @method_decorator(admin_logged)
    def get(self, request):
        name = request.GET['name']
        page_number = request.GET['pagenumber']
        page_size = request.GET['pagesize']
        query_set = client_models.WXUser.objects.filter(user_name=name).order_by('id')
        data = get_user_list(page_number, page_size, query_set)
        return JsonResponse(data=wrap_response_data(0, **data))


class ListQuestion(View):
    @method_decorator(admin_logged)
    def get(self, request):
        page_number = request.GET['pagenumber']
        page_size = request.GET['pagesize']
        que_type = request.GET['type']
        que_title = request.GET.get('title')

        if que_title is None or not que_title.strip():
            query_set = admin_models.Question.objects.filter(type=que_type).order_by('title')
        else:
            query_set = admin_models.Question.objects.filter(type=que_type, title__contains=que_title).order_by('title')

        paginator = Paginator(query_set, page_size)
        que_list = paginator.get_page(page_number).object_list
        total = query_set.count()
        serializer = ListQuestionSerializer(que_list, many=True)
        data = {'list': json.loads(json.dumps(serializer.data)),
                'total': total}
        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(admin_logged)
    def delete(self, request):
        que_id_list = request.GET.getlist('question')
        question_list = []
        try:
            for que_id in que_id_list:
                question_list.append(admin_models.Question.objects.get(id__exact=que_id))
        except Exception:
            return JsonResponse(data=wrap_response_data(3, '部分或全部题目id不存在，未执行任何删除操作'))

        for question in question_list:
            question.delete()

        return JsonResponse(data=wrap_response_data(0))


class DesignatedQuestion(View):
    @method_decorator(admin_logged)
    def get(self, request):
        que_id = request.GET['id']
        data = {}
        try:
            que = admin_models.Question.objects.get(id=que_id)
        except:
            return JsonResponse(data=wrap_response_data(3, '题目id不存在'))

        serializer = DesignatedQuestionSerializer(que)
        data = json.loads(json.dumps(serializer.data))

        sub_question_query_set = admin_models.SubQuestion.objects.filter(question__id=que_id).order_by('number')
        serializer = SubQuestionSerializer(sub_question_query_set, many=True)
        sub_question_json_list = json.loads(json.dumps(serializer.data))
        data['sub_que'] = sub_question_json_list

        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(admin_logged)
    def post(self, request):
        try:
            que_type = request.POST['type']
            que_title = request.POST['title']
            que_text = request.POST.get('text')
            sub_que_num = request.POST['sub_que_num']
        except Exception:
            return JsonResponse(data=wrap_response_data(3, 'request.POST读取父问题数据失败'))

        try:
            if que_type == CHOICE_QUE_NAME:
                new_question = admin_models.Question(type=que_type, title=que_title, sub_que_num=sub_que_num)
            else:
                new_question = admin_models.Question(type=que_type, title=que_title, sub_que_num=sub_que_num,
                                                     text=que_text)

            new_question.full_clean()

        except Exception:
            return JsonResponse(data=wrap_response_data(3, '父问题格式不正确'))

        new_sub_que_obj_list = []
        father_id = new_question.id

        sub_que_json_list = request.POST.getlist('sub_que')
        if sub_que_json_list is None or len(sub_que_json_list) != sub_que_num:
            return JsonResponse(data=wrap_response_data(3, '子问题数量不符'))

        try:
            for sub_que in sub_que_json_list:
                if que_type == CLOZE_QUE_NAME:
                    new_sub_question = admin_models.SubQuestion(question=father_id, answer=sub_que['answer'],
                                                                number=sub_que['number'],
                                                                A=sub_que['options'][0], B=sub_que['options'][1],
                                                                C=sub_que['options'][2], D=sub_que['options'][3])
                else:
                    new_sub_question = admin_models.SubQuestion(question=father_id, stem=sub_que['stem'],
                                                                answer=sub_que['answer'], number=sub_que['number'],
                                                                A=sub_que['options'][0], B=sub_que['options'][1],
                                                                C=sub_que['options'][2], D=sub_que['options'][3]
                                                                )

                new_sub_question.full_clean()
                new_sub_que_obj_list.append(new_sub_question)
        except Exception:
            return JsonResponse(data=wrap_response_data(3, '子问题格式不正确'))

        new_question.save()
        for new_sub_que in new_sub_que_obj_list:
            new_sub_que.save()

        return JsonResponse(data=wrap_response_data(0, '题目上传成功'))

    @method_decorator(admin_logged)
    def put(self, request):
        try:
            que_id = request.POST['problemid']
            que_type = request.POST['type']
            que_title = request.POST['title']
            que_text = request.POST.get('text')
            sub_que_num = request.POST['sub_que_num']
        except:
            return JsonResponse(data=wrap_response_data(3, 'request.POST读取父问题数据失败'))