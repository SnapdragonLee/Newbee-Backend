import hashlib
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import json
import requests
from .models import WXUser, WrongQuestions, ListOfQuestion
from administrator.models import Question, SubQuestion
from .serializers import client_DesignatedQuestionSerializer, client_SubQuestionSerializer
from utils.response import wrap_response_data
from django.http import JsonResponse
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from utils.auth_decorators import user_logged
from django.db import transaction
from utils.defines import *


# Create your views here.
def user_login(request):
    appid = 'wx9cb76a70a7aba68a'
    secret = 'a79c0044ff02e5368cf3bc96704f7d76'

    try:
        post_data = json.loads(request.body)
        code = post_data['code']
        wx_username = post_data['username']
    except Exception as e:
        print(e.args)
        return JsonResponse(data=wrap_response_data(3, "json格式错误"))

    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid \
          + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code'
    response = json.loads(requests.get(url).content)

    if 'errcode' in response:
        return JsonResponse(data=wrap_response_data(3, "获取openid失败"))

    openid = response['openid']
    session_key = response['session_key']

    try:
        with transaction.atomic():
            user = WXUser.objects.filter(id=openid)
            if not user:
                new_user = WXUser(id=openid, user_name=wx_username)
                new_user.save()
    except Exception as e:
        print(e.args)
        return JsonResponse(data=wrap_response_data(3, "数据库操作失败"))

    request.session['openid'] = openid
    return JsonResponse(data=wrap_response_data(0))
    # sha = hashlib.sha256()
    # sha.update(openid.encode())
    # sha.update(session_key.encode())
    # key = sha.hexdigest()
    #
    # return Response(data={'ret': 0, 'key': key})
    pass

class UserProfile(View):
    @method_decorator(user_logged)
    def get(self, request):
        open_id = request.session['openid']

        data = {}
        try:
            with transaction.atomic():
                user = WXUser.objects.get(id=open_id)
                data['username'] = user.user_name
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, "不存在为该openid的用户"))

        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(user_logged)
    def post(self, request):
        open_id = request.session['openid']

        try:
            post_data = json.loads(request.body)
            new_username = post_data['username']
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, "json格式错误"))

        try:
            with transaction.atomic():
                user = WXUser.objects.get(id=open_id)
                user.user_name = new_username
                user.save()
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, "不存在为该openid的用户"))

        return JsonResponse(data=wrap_response_data(0))


class SolutionViewClass(View):
    @method_decorator(user_logged)
    def get(self, request):
        pass

    @method_decorator(user_logged)
    def post(self, request):
        pass


@user_logged
def solution_like(request):
    try:
        post_data = json.loads(request.body)
        solution_id = post_data['solution_id']
    except Exception as e:
        print(e.args)
        return JsonResponse(data=wrap_response_data(3, 'json格式不符'))

    # todo 同一个用户对同一个题解只能点赞或举报一次


@user_logged
def solution_report(request):
    # todo 同一个用户对同一个题解只能点赞或举报一次

    pass


def return_info(this_question, question_id):
    serializer = client_DesignatedQuestionSerializer(this_question)
    data = json.loads(json.dumps(serializer.data))
    sub_question_query_set = SubQuestion.objects.filter(question__id=question_id).order_by('number')
    serializer = client_SubQuestionSerializer(sub_question_query_set, many=True)
    sub_question_json_list = json.loads(json.dumps(serializer.data))
    data['sub_que'] = sub_question_json_list
    return JsonResponse(data=wrap_response_data(0, **data))

def return_wrongquestion(user_id, question_type, user, status, status_value):
    wrong_question = WrongQuestions.objects.filter(openid=user_id, question_id__type=question_type, havedone=False).order_by('?').first()
    if not wrong_question:
        # 更新用户刷题阶段
        user.status = status - status_value
        user.save()
        # 将该用户错题表更新
        wrong_questions = WrongQuestions.objects.filter(openid=user_id)
        wrong_questions.update(havedone=False)
        # 删除该用户刷题表
        questions = ListOfQuestion.objects.filter(openid=user_id, question_id__type=question_type)
        questions.delete()
        # 从题库中随机取一个该类型题目，由于刚清空记录表，省略了一些判断
        this_question = Question.objects.filter(type=question_type).order_by('?').first()
        return return_info(this_question, this_question.id)
    # 返回随机取到的没做过的错题
    this_question = Question.objects.get(id=wrong_question.question_id)
    return return_info(this_question, wrong_question.question_id)

def return_question(type, id, user_id, user, status):
    data = {}
    if type == 'CHOICE_QUE_NAME':
        question_type = CHOICE_QUE_NAME
        all_status = [1,3,5,7]
        status_value = 1
    elif type == 'CLOZE_QUE_NAME':
        question_type=CLOZE_QUE_NAME
        all_status = [2,3,6,7]
        status_value = 2
    elif type == 'READING_QUE_NAME':
        question_type = READING_QUE_NAME
        all_status = [4,5,6,7]
        status_value = 3
    if id:#传id指定查询
        try:
            print(type)
            topic = Question.objects.get(id=id, type=question_type)
        except:
            return JsonResponse(data=wrap_response_data(3, '哦吼，本题可能已经被管理员删除啦', **data))
        return return_info(topic, id)
    else:#随机刷题
        if status in all_status:
            return return_wrongquestion(user_id, question_type, user, status, status_value)
        else:
            #获取用户已经做过的所有题目的id
            haven_do = ListOfQuestion.objects.filter(openid=user_id).values('question_id')
            #随机获取此类题型还没做过的题目
            this_question = Question.objects.filter(type=question_type).exclude(id__in=haven_do).order_by('?').first()
            if not this_question:
                user.status = status + status_value
                user.save()
                return return_wrongquestion(user_id, question_type, user, status, status_value)
            return return_info(this_question, this_question.id)


#@user_logged
def get_question(request):
    # 获取传递的参数和需要使用的数据
    question_type = request.GET.get('type')
    id = request.GET.get('id')
    user_id = 123  # request.session['openid']
    user = WXUser.objects.get(id=user_id)
    status = user.status
    return return_question(question_type, id, user_id, user, status)
