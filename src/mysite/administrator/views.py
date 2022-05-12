from django.contrib.auth import authenticate, login, logout
from utils.response import wrap_response_data
from utils.auth_decorators import admin_logged
from django.http import JsonResponse
from django.views.generic.base import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from client import models as client_models
from . import models as admin_models
from client.serializers import ListUserSerializer
from .serializers import ListQuestionSerializer, DesignatedQuestionSerializer, SubQuestionSerializer, \
    SolutionSerializer, OperationRecordSerializer, GraphDataSerializer
from django.utils.decorators import method_decorator
import json
from django.db import transaction
import datetime
from django.contrib.auth.models import User
from administrator.models import OperationRecord
from django.db.models import Q, F
from enum import Enum
from utils.defines import *


def add_operation(op_type: OperationRecord.OP_TYPE,
                  admin: User, description: str):
    new_record = OperationRecord(operation=op_type, admin=admin, description=description)
    new_record.save()


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
        sort_type = request.GET.get('sorttype')
        sort_name = request.GET.get('sortname')

        name_map = {
            'numc': 'total_cloze',
            'numm': 'total_choice',
            'numr': 'total_reading'
        }

        if sort_name is None or sort_type is None:
            order_method_str = 'user_name'
        else:
            order_method_str = name_map[sort_name]
            if int(sort_type) == 0:
                order_method_str = '-' + order_method_str

        query_set = client_models.WXUser.objects.all().order_by(order_method_str)

        data = get_user_list(page_number, page_size, query_set)
        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(admin_logged)
    def delete(self, request):
        id_list = request.GET.getlist('userid')  # 根据赵佬的提醒获取DELETE的参数也得用GET

        try:
            with transaction.atomic():
                for user_id in id_list:
                    wxuser_obj = client_models.WXUser.objects.get(id=user_id)
                    add_operation(OperationRecord.OP_TYPE.DEL, request.user, '小程序用户: ' + wxuser_obj.user_name)
                    wxuser_obj.delete()
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
        serializer = ListQuestionSerializer(que_list, many=True, context={'admin': request.user})
        data = {'list': json.loads(json.dumps(serializer.data)),
                'total': total}
        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(admin_logged)
    def delete(self, request):
        que_id_list = request.GET.getlist('question')

        try:
            with transaction.atomic():
                for que_id in que_id_list:
                    que_obj = admin_models.Question.objects.get(id__exact=que_id)
                    add_operation(OperationRecord.OP_TYPE.DEL, request.user, que_obj.title)
                    que_obj.delete()
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

        sub_question_query_set = que.subquestion_set.order_by('number')
        serializer = SubQuestionSerializer(sub_question_query_set, many=True, context={'admin': request.user})
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

        add_operation(OperationRecord.OP_TYPE.ADD, request.user, new_question.title)
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

                child_query_set = admin_models.SubQuestion.objects.filter(question_id=father_id).order_by('number')

                i = 0
                while i < new_child_cnt:
                    stem = child_input_list[i]['stem']
                    A = child_input_list[i]['options'][0]
                    B = child_input_list[i]['options'][1]
                    C = child_input_list[i]['options'][2]
                    D = child_input_list[i]['options'][3]
                    answer = child_input_list[i]['answer']
                    number = child_input_list[i]['number']

                    if i < old_child_cnt:
                        child_object = child_query_set[i]
                        child_object.stem = stem
                        child_object.A = A
                        child_object.B = B
                        child_object.C = C
                        child_object.D = D
                        child_object.answer = answer
                        child_object.number = number
                    else:
                        child_object = admin_models.SubQuestion(question=father, stem=stem,
                                                                answer=answer, number=number,
                                                                A=A, B=B, C=C, D=D)

                    child_object.save()
                    i += 1

                while i < old_child_cnt:
                    child_query_set[i].delete()
                    i += 1

        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '题目格式错误'))

        add_operation(OperationRecord.OP_TYPE.MOD, request.user, father.title)
        return JsonResponse(data=wrap_response_data(0, '修改成功'))


class ListSolution(View):
    @method_decorator(admin_logged)
    def get(self, request):
        try:
            sub_que_id = request.GET['sub_question_id']
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '获取题解时，提供的参数格式有误'))

        query_set = admin_models.Solution.objects.filter(subQuestion_id=sub_que_id).order_by('-reports')

        # total = query_set.count()
        total = len(query_set)
        serializer = SolutionSerializer(query_set, many=True, context={'request': request})

        data = {'solutions': json.loads(json.dumps(serializer.data)),
                'total': total}

        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(admin_logged)
    def delete(self, request):

        solution_id_list = request.GET.getlist('id')

        try:
            sub_que_obj = admin_models.Solution.objects.get(id=solution_id_list[0]).subQuestion
            que_obj = sub_que_obj.question
            with transaction.atomic():
                for solution_id in solution_id_list:
                    admin_models.Solution.objects.get(id=solution_id).delete()

        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, "有部分或全部题解id不合法，未执行任何删除操作"))

        # add_operation(OperationRecord.OP_TYPE.DEL, request.user, que_obj.title + '  第' + str(sub_que_obj.number) + '小题题解')
        return JsonResponse(data=wrap_response_data(0))

    @method_decorator(admin_logged)
    def post(self, request):
        try:
            post_data = json.loads(request.body)
            solution_id = post_data['solution_id']
        except Exception as e:
            print(e)
            return JsonResponse(data=wrap_response_data(3, 'json参数格式错误'))

        if admin_models.AdminApproveSolution.objects.filter(admin=request.user, solution_id=solution_id).exists():
            return JsonResponse(data=wrap_response_data(3, '您已经确认过此题解'))

        try:
            with transaction.atomic():
                admin_models.AdminApproveSolution.objects.create(admin=request.user, solution_id=solution_id)
                solution_obj = admin_models.Solution.objects.get(id__exact=solution_id)
                solution_obj.add_approval()
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '题解id有误'))

        return JsonResponse(data=wrap_response_data(0))


@admin_logged
def has_bad_solution(request):
    bad_solution_sum = admin_models.Solution.objects.filter(is_bad=True).count()
    approved_bad_solution_num = admin_models.AdminApproveSolution.objects.filter(admin=request.user,
                                                                                 solution__is_bad=True).count()
    has = 0 if bad_solution_sum == approved_bad_solution_num else 1
    data = {'has_bad_solution': has}

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
                'time': str(notice_obj.time + datetime.timedelta(hours=8)).split('.')[0]}

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

        add_operation(OperationRecord.OP_TYPE.MOD, request.user, '公告')
        return JsonResponse(data=wrap_response_data(0))
        pass


def get_operation_record(request):
    try:
        page_num = request.GET['pagenumber']
        page_size = request.GET['pagesize']
    except Exception as e:
        print(e.args)
        return JsonResponse(data=wrap_response_data(3, "json参数格式错误"))

    query_set = OperationRecord.objects.all()
    total = query_set.count()
    paginator = Paginator(query_set, page_size)
    op_record_list = paginator.get_page(page_num).object_list
    serializer = OperationRecordSerializer(op_record_list, many=True)
    data = {"records": json.loads(json.dumps(serializer.data)),
            "total": total}

    return JsonResponse(data=wrap_response_data(0, **data))


def serialize_top_users(field_name: str):
    top_users = client_models.WXUser.objects.all().order_by(field_name)[0:5]
    serializer = GraphDataSerializer(top_users, many=True, context={'field_name': field_name})
    return json.loads(json.dumps(serializer.data))


def get_graph_data(request):
    user_sum = client_models.WXUser.objects.all().count()
    choice_sum = admin_models.Question.objects.filter(type=CHOICE_QUE_NAME).count()
    cloze_sum = admin_models.Question.objects.filter(type=CLOZE_QUE_NAME).count()
    reading_sum = admin_models.Question.objects.filter(type=READING_QUE_NAME).count()
    question_sum = choice_sum + cloze_sum + reading_sum
    bad_solution_sum = admin_models.Solution.objects.filter(is_bad=True).count()
    approved_bad_solution_sum = admin_models.AdminApproveSolution.objects.filter(admin=request.user,
                                                                                 solution__is_bad=True).count()
    unapproved_bad_solution_sum = bad_solution_sum - approved_bad_solution_sum

    data = {"usernumber": user_sum, "questionnumber": question_sum, "bad_solution_number": unapproved_bad_solution_sum,
            "questions_number": [
                {
                    'value': choice_sum,
                    'name': '单项选择'
                },
                {
                    'value': cloze_sum,
                    'name': '完形填空'
                },
                {
                    'value': reading_sum,
                    'name': '阅读理解'
                }
            ], 'choice_question_top5': serialize_top_users('total_choice'),
            'cloze_question_top5': serialize_top_users('total_cloze'),
            'reading_question_top5': serialize_top_users('total_reading')}

    return JsonResponse(data=wrap_response_data(0, **data))
