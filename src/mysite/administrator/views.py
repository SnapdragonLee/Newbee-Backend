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
from .serializers import ListQuestionSerializer, DesignatedQuestionSerializer, SubQuestionSerializer, SolutionSerializer
from django.utils.decorators import method_decorator
import json
from utils.defines import *
from django.db import transaction


# Create your views here.
def admin_login(request):
    post_data = json.loads(request.body)
    username = post_data['name']
    password = post_data['pwd']
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

    # total = query_set.count()
    total = len(query_set)
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
        # total = query_set.count()
        total = len(query_set)
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
            post_data = json.loads(request.body)
            que_type = post_data['type']
            que_title = post_data['title']
            que_text = post_data.get('text')
            sub_que_num = post_data['sub_que_num']
            sub_que_json_list = post_data['sub_que']
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '提供的参数名称不对，或缺少所需参数'))

        if sub_que_json_list is None or len(sub_que_json_list) != sub_que_num:
            raise Exception("子题目数量不符")

        try:
            with transaction.atomic():
                new_question = admin_models.Question(type=que_type, title=que_title,
                                                     sub_que_num=sub_que_num, text=que_text)

                new_question.save()

                for sub_que in sub_que_json_list:
                    new_sub_question = admin_models.SubQuestion(question=new_question,
                                                                stem=sub_que.get('stem'),
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
            post_data = json.loads(request.body)
            father_id = post_data['problemid']
            father_type = post_data['type']
            father_title = post_data['title']
            father_text = post_data.get('text')
            father_sub_que_num = post_data['sub_que_num']
            child_input_list = post_data['sub_que']
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '提供的参数名称不对，或缺少所需参数'))

        if child_input_list is None or len(child_input_list) != father_sub_que_num:
            return JsonResponse(data=wrap_response_data(3, '子题目数量不符'))

        child_input_list.sort(key=lambda child: child['number'])

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
                        child_object = admin_models.SubQuestion(question=father, stem=stem,
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


class ListSolution(View):
    @method_decorator(admin_logged)
    def get(self, request):
        try:
            sub_que_id = request.GET['sub_question_id']
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '获取题解时，提供的参数格式有误'))

        query_set = admin_models.Solution.objects.filter(subQuestion__id=sub_que_id).order_by('-reports')

        # total = query_set.count()
        total = len(query_set)
        serializer = SolutionSerializer(query_set, many=True)

        data = {'solutions': json.loads(json.dumps(serializer.data)),
                'total': total}

        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(admin_logged)
    def delete(self, request):

        solution_id_list = request.GET.getlist('id')

        try:
            with transaction.atomic():
                for solution_id in solution_id_list:
                    admin_models.Solution.objects.get(id=solution_id).delete()

        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, "有部分或全部题解id不合法，未执行任何删除操作"))

        return JsonResponse(data=wrap_response_data(0))


@admin_logged
def has_bad_solution(request):
    query_set = admin_models.Solution.objects.all()
    has = False
    for solution in query_set:
        if solution.is_bad_solution():
            has = True
            break

    if has:
        data = {'has_bad_solution': 1}
    else:
        data = {'has_bad_solution': 0}

    return JsonResponse(data=wrap_response_data(0, **data))


def check_has_notice():
    return True if admin_models.Notice.objects.count() >= 1 else False


class NoticeViewClass(View):
    @method_decorator(admin_logged)
    def get(self, request):

        if not check_has_notice():
            notice_obj = admin_models.Notice()
            notice_obj.save()
        else:
            notice_obj = admin_models.Notice.objects.all()[0]

        data = {'content': notice_obj.content,
                'time': str(notice_obj.time).split('.')[0]}

        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(admin_logged)
    def post(self, request):
        try:
            post_data = json.loads(request.body)
            content = post_data['content']
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, 'json格式错误'))

        if not check_has_notice():
            notice_obj = admin_models.Notice()
        else:
            notice_obj = admin_models.Notice.objects.all()[0]

        notice_obj.content = content
        notice_obj.save()
        return JsonResponse(data=wrap_response_data(0))
        pass
