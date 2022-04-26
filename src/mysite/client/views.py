import hashlib
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import json
import requests
from .models import WXUser
from utils.response import wrap_response_data
from django.http import JsonResponse


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
