import json
import datetime
import requests

from django.http import JsonResponse
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.db import transaction
from django.core.paginator import Paginator

from .models import WrongQuestions, ListOfQuestion, history, done_question, UserApproveSolution
from models.basic.user import WXUser
from models.basic.notice import Notice
from models.basic.questions import Question, SubQuestion, Solution
from .serializers import client_DesignatedQuestionSerializer, client_SubQuestionSerializer, \
    client_ListQuestionSerializer, AnswerSerializer, ClientSolutionSerializer, \
    client_DetailSerializer

from utils.response import wrap_response_data
from utils.auth_decorators import user_logged
from utils.defines import *

from mysite.settings import APPID, SECRET


# Create your views here.

def user_login(request):
    appid = APPID
    secret = SECRET

    try:
        post_data = json.loads(request.body)
        code = post_data['code']
        wx_username = post_data['username']
    except Exception as e:
        print(e.args)
        return JsonResponse(data=wrap_response_data(3, 'json格式错误'))

    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid \
          + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code'
    print(code)
    response = json.loads(requests.get(url).content)

    if 'errcode' in response:
        return JsonResponse(data=wrap_response_data(3, '获取openid失败'))

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
        return JsonResponse(data=wrap_response_data(3, '数据库操作失败'))

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
            return JsonResponse(data=wrap_response_data(3, '不存在为该openid的用户'))

        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(user_logged)
    def post(self, request):
        open_id = request.session['openid']

        try:
            post_data = json.loads(request.body)
            new_username = post_data['username']
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, 'json格式错误'))

        try:
            with transaction.atomic():
                user = WXUser.objects.get(id=open_id)
                user.user_name = new_username
                user.save()
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '不存在为该openid的用户'))

        return JsonResponse(data=wrap_response_data(0))


class SolutionViewClass(View):
    @method_decorator(user_logged)
    def get(self, request):
        try:
            sub_que_id = request.GET['id']
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, 'json参数格式错误'))

        solution_list = Solution.objects.filter(subQuestion__id=sub_que_id).order_by('-likes')
        serializer = ClientSolutionSerializer(solution_list, many=True, context={'openid': request.session['openid']})
        num = len(solution_list)
        data = {'solution_num': num,
                'solution': json.loads(json.dumps(serializer.data))}

        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(user_logged)
    def post(self, request):
        try:
            post_data = json.loads(request.body)
            sub_que_id = post_data['id']
            content = post_data['solution']
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, 'json参数格式错误'))

        try:
            sub_que_obj = SubQuestion.objects.get(id__exact=sub_que_id)
        except Exception as e:
            print(e.args)
            return JsonResponse(data=wrap_response_data(3, '不存在为该id的子题目'))

        wx_user = WXUser.objects.get(id__exact=request.session['openid'])
        Solution.objects.create(subQuestion=sub_que_obj, wxUser=wx_user,
                                content=content)
        wx_user.add_solution_sum()

        return JsonResponse(data=wrap_response_data(0))


@user_logged
def solution_like(request):
    try:
        post_data = json.loads(request.body)
        solution_id = post_data['id']
    except Exception as e:
        print(e.args)
        return JsonResponse(data=wrap_response_data(3, 'json格式不符'))

    user = WXUser.objects.get(id=request.session['openid'])

    if UserApproveSolution.objects.filter(user=user, solution__id=solution_id).exists():
        return JsonResponse(data=wrap_response_data(3, '已经点赞或举报过'))

    try:
        with transaction.atomic():
            solution = Solution.objects.get(id=solution_id)
            solution.add_like()
            UserApproveSolution.objects.create(user=user, solution=solution, type=UserApproveSolution.Type.LIKE)
    except Exception as e:
        print(e.args)
        return JsonResponse(data=wrap_response_data(3, '题解id不合法'))

    return JsonResponse(data=wrap_response_data(0))


@user_logged
def solution_report(request):
    try:
        post_data = json.loads(request.body)
        solution_id = post_data['id']
    except Exception as e:
        print(e.args)
        return JsonResponse(data=wrap_response_data(3, 'json格式不符'))

    user = WXUser.objects.get(id=request.session['openid'])

    if UserApproveSolution.objects.filter(user=user, solution__id=solution_id).exists():
        return JsonResponse(data=wrap_response_data(3, '已经点赞或举报过'))

    try:
        with transaction.atomic():
            solution = Solution.objects.get(id=solution_id)
            solution.add_report()
            UserApproveSolution.objects.create(user=user, solution=solution, type=UserApproveSolution.Type.REPORT)
    except Exception as e:
        print(e.args)
        return JsonResponse(data=wrap_response_data(3, '题解id不合法'))

    return JsonResponse(data=wrap_response_data(0))


def return_info(this_question, question_id, flag):
    serializer = client_DesignatedQuestionSerializer(this_question)
    data = json.loads(json.dumps(serializer.data))
    sub_question_query_set = SubQuestion.objects.filter(question__id=question_id).order_by('number')
    serializer = client_SubQuestionSerializer(sub_question_query_set, many=True)
    sub_question_json_list = json.loads(json.dumps(serializer.data))
    data['sub_que'] = sub_question_json_list
    data['flag'] = flag
    return JsonResponse(data=wrap_response_data(0, **data))


def return_wrongquestion(user_id, question_type, user, status, status_value):
    wrong_question = WrongQuestions.objects.filter(openid=user_id, question__type=question_type,
                                                   havedone=False).order_by('?').first()
    if not wrong_question:
        # 更新用户刷题阶段
        user.status = status - status_value
        user.save()
        # 将该用户错题表更新
        wrong_questions = WrongQuestions.objects.filter(openid=user_id)
        wrong_questions.update(havedone=False)
        # 删除该用户刷题表
        questions = ListOfQuestion.objects.filter(openid=user_id, question__type=question_type)
        questions.delete()
        # 从题库中随机取一个该类型题目，由于刚清空记录表，省略了一些判断
        this_question = Question.objects.filter(type=question_type).order_by('?').first()
        flag = 0
        return return_info(this_question, this_question.id, flag)
    # 返回随机取到的没做过的错题
    this_question = Question.objects.get(id=wrong_question.question_id)
    flag = 1
    return return_info(this_question, wrong_question.question_id, flag)


def return_question(type, id, user_id, user, status):
    data = {}
    if type == 'choice_question':
        question_type = CHOICE_QUE_NAME
        all_status = [1, 3, 5, 7]
        status_value = 1
    elif type == 'cloze_question':
        question_type = CLOZE_QUE_NAME
        all_status = [2, 3, 6, 7]
        status_value = 2
    elif type == 'reading_question':
        question_type = READING_QUE_NAME
        all_status = [4, 5, 6, 7]
        status_value = 3
    else:
        return JsonResponse(data=wrap_response_data(3, 'type error', **data))
    if id:  # 传id指定查询
        try:
            topic = Question.objects.get(id=id, type=question_type)
        except:
            return JsonResponse(data=wrap_response_data(3, '哦吼，本题可能已经被管理员删除啦', **data))
        flag = 0
        return return_info(topic, id, flag)
    else:  # 随机刷题
        if status in all_status:
            return return_wrongquestion(user_id, question_type, user, status, status_value)
        else:
            # 获取用户已经做过的所有题目的id
            haven_do = ListOfQuestion.objects.filter(openid=user_id).values('question__id')
            # 随机获取此类题型还没做过的题目
            this_question = Question.objects.filter(type=question_type).exclude(id__in=haven_do).order_by('?').first()
            if not this_question:
                user.status = status + status_value
                status = user.status
                user.save()
                return return_wrongquestion(user_id, question_type, user, status, status_value)
            flag = 0
            return return_info(this_question, this_question.id, flag)


@user_logged
def get_question(request):
    # 获取传递的参数和需要使用的数据
    question_type = request.GET['type']
    id = request.GET.get('id')
    user_id = request.session['openid']
    user = WXUser.objects.get(id=user_id)
    status = user.status
    return return_question(question_type, id, user_id, user, status)


class wrong_que_bookClass(View):
    @method_decorator(user_logged)
    def get(self, request):
        page_number = request.GET['pagenumber']
        page_size = 12
        user_id = request.session['openid']
        type = request.GET.get('type')
        if not type:
            wrong_question_list = WrongQuestions.objects.filter(openid=user_id).order_by('-date')
        else:
            wrong_question_list = WrongQuestions.objects.filter(openid=user_id, question__type=type).order_by('-date')
        # if not wrong_question_list:
        #    return JsonResponse(data=wrap_response_data(3, '目前还没有错题加入哦'))
        total = len(wrong_question_list)
        paginator = Paginator(wrong_question_list, page_size)
        que_list = paginator.get_page(page_number).object_list
        serializer = client_ListQuestionSerializer(que_list, many=True)
        data = {'list': json.loads(json.dumps(serializer.data)),
                'total': total}
        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(user_logged)
    def post(self, request):
        user_id = request.session['openid']
        id = request.GET['id']
        if WrongQuestions.objects.filter(openid=user_id, question_id=id).exists():
            return JsonResponse(data=wrap_response_data(3, '错题本中已经有这个题目了'))

        WrongQuestions.objects.create(openid=user_id, question_id=id)
        return JsonResponse(data=wrap_response_data(0))

    @method_decorator(user_logged)
    def delete(self, request):
        user_id = request.session['openid']
        id = request.GET['id']
        try:
            wrong_question = WrongQuestions.objects.get(openid=user_id, question_id=id)
        except:
            return JsonResponse(data=wrap_response_data(3, '错题本查询不到对应题目'))
        wrong_question.delete()
        return JsonResponse(data=wrap_response_data(0))


class NoticeViewClass(View):
    def get(self, request):
        if Notice.objects.count() >= 1:
            notice_obj = Notice.objects.all()[0]
            data = {'content': notice_obj.content,
                    'time': str(notice_obj.time + datetime.timedelta(hours=8)).split('.')[0]}
            return JsonResponse(data=wrap_response_data(0, **data))
        else:
            return JsonResponse(data=wrap_response_data(3, '今天测试核酸了吗? 没测试就跑来搞英语? 这是一条默认公告'))


class recordClass(View):
    @method_decorator(user_logged)
    def get(self, request):
        user_id = request.session['openid']
        type = request.GET.get('type')
        page_number = request.GET['pagenumber']
        page_size = 12
        if not type:
            question_list = history.objects.filter(openid=user_id).order_by('-date')
        else:
            question_list = history.objects.filter(openid=user_id, question__type=type).order_by('-date')
        total = len(question_list)
        paginator = Paginator(question_list, page_size)
        que_list = paginator.get_page(page_number).object_list
        serializer = client_ListQuestionSerializer(que_list, many=True)
        data = {'list': json.loads(json.dumps(serializer.data)),
                'total': total}
        return JsonResponse(data=wrap_response_data(0, **data))

    @method_decorator(user_logged)
    def delete(self, request):
        user_id = request.session['openid']
        done_questions = ListOfQuestion.objects.filter(openid=user_id)
        done_questions.delete()
        question_history = history.objects.filter(openid=user_id)
        question_history.delete()
        wrong_questions = WrongQuestions.objects.filter(openid=user_id)
        wrong_questions.update(havedone=False)
        return JsonResponse(data=wrap_response_data(0))


@user_logged
def single_history(request):
    user_id = request.session['openid']
    id = request.GET['id']
    date = request.GET['date']
    delete_history = history.objects.get(openid=user_id, question_id=id, date=date)
    delete_history.delete()
    question = ListOfQuestion.objects.get(openid=user_id, question_id=id)
    question.delete()
    return JsonResponse(data=wrap_response_data(0))

@user_logged
def detail(request):
    user_id = request.session['openid']
    id = request.GET['id']
    try:
        question = Question.objects.get(id=id)
    except:
        return JsonResponse(data=wrap_response_data(3, '查询不到该题目，可能被管理员删除了.,.'))

    serializer = client_DesignatedQuestionSerializer(question)
    data = json.loads(json.dumps(serializer.data))
    sub_question_query_set = SubQuestion.objects.filter(question__id=id).order_by('number')
    serializer = client_DetailSerializer(sub_question_query_set, many=True, context={'openid': user_id})
    sub_question_json_list = json.loads(json.dumps(serializer.data))
    data['sub_que'] = sub_question_json_list

    return JsonResponse(data=wrap_response_data(0, **data))


@user_logged
def check_question(request):
    user_id = request.session['openid']

    post_data = json.loads(request.body)
    id = post_data['id']
    type = post_data['type']
    post = post_data['data']

    history.objects.create(openid=user_id, question_id=id)
    ListOfQuestion.objects.create(openid=user_id, question_id=id)
    answers = SubQuestion.objects.filter(question_id=id).values('number', 'answer')

    if answers.exists() is False:
        return JsonResponse(data=wrap_response_data(3, '没有对应的小题答案'))

    WXsubmit = WXUser.objects.get(id=user_id)

    i = 0
    for item in post:
        if type == CHOICE_QUE_NAME:
            if item['submit'] == answers[i]['answer']:
                WXsubmit.right_choice += 1
            WXsubmit.total_choice += 1

        elif type == CLOZE_QUE_NAME:
            if item['submit'] == answers[i]['answer']:
                WXsubmit.right_cloze += 1
            WXsubmit.total_cloze += 1

        else:
            if item['submit'] == answers[i]['answer']:
                WXsubmit.right_reading += 1
            WXsubmit.total_reading += 1

        try:
            obj = done_question.objects.get(wxUser_id=user_id, subQuestion_id=item['sub_id'])
            obj.option = item['submit']
            obj.save()
        except:
            done_question.objects.create(wxUser_id=user_id, question_id=post_data['id'],
                                         subQuestion_id=item['sub_id'], option=item['submit'])

        i += 1

    WXsubmit.save()

    sub = SubQuestion.objects.filter(question_id=id)
    serializer = AnswerSerializer(sub, many=True)

    data = {
        'sub_que': json.loads(json.dumps(serializer.data))
    }

    return JsonResponse(data=wrap_response_data(0, **data))


@user_logged
def statistics(request):
    user_id = request.session['openid']
    WXsubmit = WXUser.objects.get(id=user_id)

    data = {
        'choice_num': WXsubmit.total_choice,
        'choice_right': WXsubmit.right_choice,
        'cloze_num': WXsubmit.total_cloze,
        'cloze_right': WXsubmit.right_cloze,
        'reading_num': WXsubmit.total_reading,
        'reading_right': WXsubmit.right_reading,
    }

    return JsonResponse(data=wrap_response_data(0, **data))
