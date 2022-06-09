import json
import requests
from urllib import parse

import mysite.settings as ms

login_api = 'https://aip.baidubce.com/oauth/2.0/token'
test_api = 'https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined'

baidu_sensor_access_token = ""

gLogin_data = {
    'grant_type': ms.baidu_sensor_grant_type,
    'client_id': ms.baidu_sensor_id,
    'client_secret': ms.baidu_sensor_secret
}

gTest_data = {
    'access_token': baidu_sensor_access_token,
    'text': ''
}

headerB = {'Content-Type': 'application/x-www-form-urlencoded'}

req = requests.session()


def encode_formdata(obj):
    str_t = []
    for key in obj:
        str_t.append(parse.unquote(key) + '=' + parse.unquote(obj[key]))

    return_str = '&'.join(str_t)
    return return_str


def login():
    login_data = encode_formdata(gLogin_data)
    resp = req.post(url=login_api, headers=headerB, data=login_data)

    if resp.status_code == 200:
        verify = json.loads(resp.content.decode('utf-8'), parse_int=str)
        global baidu_sensor_access_token
        baidu_sensor_access_token = verify['access_token']


def sensor(obj: str):
    return_data = {
        'status': '',
        'invalid_reason': []
    }

    for i in range(0, 5):
        gTest_data['text'] = obj
        test_data = encode_formdata(gTest_data).encode('utf8')
        resp = req.post(url=test_api, headers=headerB, data=test_data)

        if resp.status_code == 200:
            verify = json.loads(resp.content.decode('utf-8'), parse_int=str)

            if 'error_code' in verify.keys():
                login()
                continue

            elif verify['conclusionType'] == '1':
                return_data['status'] = '1'

            elif verify['conclusionType'] == '2':
                return_data['status'] = '0'
                for key in verify['data']:
                    return_data['invalid_reason'].append(key['msg'])

            return return_data

        else:
            return_data['status'] = '0'
            return_data['invalid_reason'].append('服务器无网络连接，请联系后台管理员')
            return return_data

    return_data['status'] = '1'
    return_data['invalid_reason'].append('服务器产生未知错误，请联系ld检查这部分什么问题')
    return return_data
    pass
