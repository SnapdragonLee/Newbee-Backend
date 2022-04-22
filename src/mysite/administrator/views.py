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
from django.db import transaction
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

        try:
            with transaction.atomic():
                for user_id in id_list:
                    client_models.WXUser.objects.get(id=user_id).delete()
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '部分或全部用户id不存在，未执行任何删除操作'))

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

        try:
            with transaction.atomic():
                for que_id in que_id_list:
                    admin_models.Question.objects.get(id__exact=que_id).delete()
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '部分或全部题目id不存在，未执行任何删除操作'))

        return JsonResponse(data=wrap_response_data(0))


class DesignatedQuestion(View):
    @method_decorator(admin_logged)
    def get(self, request):
        que_id = request.GET['id']
        try:
            que = admin_models.Question.objects.get(id=que_id)
        except Exception as e:
            print(e.args)
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
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, 'request.POST读取父题目数据失败'))

        try:
            with transaction.atomic():
                new_question = admin_models.Question(type=que_type, title=que_title,
                                                     sub_que_num=sub_que_num, text=que_text)

                new_question.save()

                father_id = new_question.id
                sub_que_json_list = request.POST.getlist('sub_que')
                if sub_que_json_list is None or len(sub_que_json_list) != sub_que_num:
                    raise Exception("子题目数量不符")

                for sub_que in sub_que_json_list:
                    new_sub_question = admin_models.SubQuestion(question=father_id,
                                                                stem=sub_que.get('stem', default=None),
                                                                answer=sub_que['answer'], number=sub_que['number'],
                                                                A=sub_que['options'][0], B=sub_que['options'][1],
                                                                C=sub_que['options'][2], D=sub_que['options'][3]
                                                                )

                    new_sub_question.save()
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '题目格式不正确'))

        return JsonResponse(data=wrap_response_data(0, '题目上传成功'))

    @method_decorator(admin_logged)
    def put(self, request):
        try:
            father_id = request.POST['problemid']
            father_type = request.POST['type']
            father_title = request.POST['title']
            father_text = request.POST.get('text')
            father_sub_que_num = request.POST['sub_que_num']
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, 'request.POST读取父题目数据失败'))

        try:
            father = admin_models.Question.objects.get(id=father_id)
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '不存在为该id的题目'))

        try:
            with transaction.atomic():
                old_child_cnt = father.sub_que_num
                new_child_cnt = father_sub_que_num

                father.type = father_type
                father.title = father_title
                father.text = father_text
                father.sub_que_num = father_sub_que_num
                father.save()

                child_query_set = admin_models.SubQuestion.objects.filter(question__id=father_id).order_by('number')

                child_input_list = request.POST.get['sub_que']
                if child_input_list is None or len(child_input_list) != father_sub_que_num:
                    raise Exception('子题目数量错误')
                child_input_list.sort(key=lambda child: child['number'])

                i = 0
                while i < new_child_cnt:
                    stem = child_input_list[i]['stem']
                    A = child_input_list[i]['options'][0]
                    B = child_input_list[i]['options'][1]
                    C = child_input_list[i]['options'][2]
                    D = child_input_list[i]['options'][3]
                    answer = child_input_list[i]['answer']

                    if i < old_child_cnt:
                        child_object = child_query_set[i]
                        child_object.stem = stem
                        child_object.A = A
                        child_object.B = B
                        child_object.C = C
                        child_object.D = D
                        child_object.answer = answer
                    else:
                        child_object = admin_models.SubQuestion(question=father_id, stem=stem,
                                                                answer=answer, number=i + 1,
                                                                A=A, B=B, C=C, D=D)

                    child_object.save()
                    i += 1

                while i < old_child_cnt:
                    child_query_set[i].delete()
                    i += 1

        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '题目格式错误'))

        return JsonResponse(data=wrap_response_data(0, '修改成功'))