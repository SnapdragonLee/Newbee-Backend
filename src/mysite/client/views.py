import hashlib
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import json
import requests
from .models import WXUser
from utils.response import wrap_response_data
from django.http import JsonResponse
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from utils.auth_decorators import user_logged
from django.db import transaction


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
