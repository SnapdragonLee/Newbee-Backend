import requests
import json
import time
from urllib import parse

login_api = "https://aip.baidubce.com/oauth/2.0/token"
test_api = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"

gLogin_data = {
    "grant_type": "",
    "client_id": "",
    "client_secret": ""
}

headerB = {"Content-Type": "application/x-www-form-urlencoded"}

gTest_data = {
    "access_token": "",
    "text": ""
}

invalid_reason = []

# --------------------------------------------------------------------#

req = requests.Session()


def out(str):
    print(time.strftime("%Y.%m.%d %H:%M:%S: ", time.localtime(time.time())) + str)


def encode_formdata(obj):
    str = []
    for key in obj:
        str.append(parse.unquote(key) + "=" + parse.unquote(obj[key]))

    return_str = "&".join(str)
    return return_str


def test():
    # print(profile)
    out("The api address is at：%s\n" % test_api)
    out("Test starting...")
    test_data = encode_formdata(gTest_data).encode('utf8')

    # admin_login
    resp = req.post(url=test_api, headers=headerB, data=test_data)

    if resp.status_code == 200:
        verify = json.loads(resp.content.decode("utf-8"), parse_int=str)
        out("return data：%s \n" % verify)
        out("return message(msg)：%s" % verify["conclusion"])
        for obj in verify["data"]:
            invalid_reason.append(obj["msg"])

        out("reason list：%s" % invalid_reason)

    else:
        out("page response: %d, operation failed" % resp.status_code)


def login():
    out("Start to login...")

    login_data = encode_formdata(gLogin_data)
    resp = req.post(url=login_api, headers=headerB, data=login_data)

    if resp.status_code == 200:
        verify = json.loads(resp.content.decode("utf-8"), parse_int=str)
        out("return access_token：%s, login attempt success!" % verify["access_token"])
        gTest_data["access_token"] = verify["access_token"]

    else:
        out("page response：%d, login failed!" % resp.status_code)


if __name__ == "__main__":
    login()
    test()
