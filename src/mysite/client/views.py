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


# Create your views here.
def user_login(request):
    appid = 'wx9cb76a70a7aba68a'
    secret = 'a79c0044ff02e5368cf3bc96704f7d76'
    post_data = json.loads(request.body)
    code = post_data['code']

    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid \
          + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code'
    response = json.loads(requests.get(url).content)

    if 'errcode' in response:
        return JsonResponse(data=wrap_response_data(3, "获取openid失败"))

    openid = response['openid']
    session_key = response['session_key']

    user = WXUser.objects.filter(id=openid)
    if not user:
        new_user = WXUser(id=openid, user_name='默认用户名')
        new_user.save()

    request.session['openid'] = openid
    return JsonResponse(data=wrap_response_data(0))
    # sha = hashlib.sha256()
    # sha.update(openid.encode())
    # sha.update(session_key.encode())
    # key = sha.hexdigest()
    #
    # return Response(data={'ret': 0, 'key': key})
    pass


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
        return JsonResponse(data=wrap_response_data(3, '参数格式不符'))

    # todo 同一个用户对同一个题解只能点赞或举报一次


@user_logged
def solution_report(request):
    # todo 同一个用户对同一个题解只能点赞或举报一次

    pass
