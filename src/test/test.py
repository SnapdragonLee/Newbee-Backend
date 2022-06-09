import os
import requests
import json
import time
from urllib import parse

test_actor = "client"  # something like "admin" \ "client"
test_profile = "solution"  # you need to create json file in profile documents

main_addr = "http://127.0.0.1:8000"  # local server location
# main_addr = "http://122.9.32.180"  # remote server location

##################################################################################################

test_profile_path = os.path.abspath(r"./" + test_actor + "/profile/" + test_profile + ".json")
profile = json.load(open(test_profile_path, "rb"), parse_int=str)

gLogin_data = profile["login_data"]
gLogin_url = main_addr + "/api/user/login"

test_api = main_addr + profile["test_api"]
# You can simulate many choices like "gLogin_url":
profile_type = profile["type"]
profile_data = profile["data"]

session = requests.session()

##################################################################################################


print("\n"
      "**************************************************\n"
      "*     Newbee-English Script Test (Dev v0.12)     *\n"
      "**************************************************\n")


def out(str):
    print(time.strftime("%Y.%m.%d %H:%M:%S: ", time.localtime(time.time())) + str)


def encode_formdata(obj):
    str = []
    for key in obj:
        str.append(parse.unquote(key) + "=" + parse.unquote(obj[key]))

    return_str = "&".join(str)
    return return_str


def check_req(req: requests.Session, type: str, url: str, headers, data=None):
    if type == "get":
        return req.get(url=url, headers=headers)

    elif type == "put":
        return req.put(url=url, headers=headers, data=data)

    elif type == "delete":
        return req.delete(url=url, headers=headers)

    elif type == "post":
        return req.post(url=url, headers=headers, data=data)

    elif type == "patch":
        return req.patch(url=url, headers=headers, data=data)


def login():
    out("Start to login...")

    header = {"Content-Type": "application/json"}
    login_data = json.dumps(gLogin_data)  # encode_formdata(userdata)
    resp = check_req(req=session, type="post", url=gLogin_url, headers=header, data=login_data)

    if resp.status_code == 200:
        verify = json.loads(resp.content.decode("utf-8"), parse_int=str)
        out("return code(ret)：%s, login attempt success!" % verify["ret"])
        out("return message(msg)：%s" % verify["msg"])

    else:
        out("page response：%d, login failed!" % resp.status_code)


def test():
    # print(profile)
    out("The api address is at：%s\n" % test_api)
    out("Test starting...")

    header = {"Content-Type": "application/json"}
    test_data = json.dumps(profile_data)  # encode_formdata(userdata)

    # admin_login
    resp = check_req(req=session, type=profile_type, url=test_api, headers=header, data=test_data)

    if resp.status_code == 200:
        verify = json.loads(resp.content.decode("utf-8"), parse_int=str)
        out("return data：%s \n" % verify)
        out("return code(ret)：%s，backend considered this situation!" % verify["ret"])
        out("return message(msg)：%s" % verify["msg"])

    else:
        out("page response: %d, operation failed" % resp.status_code)


if __name__ == "__main__":
    # login()
    print("\n")
    test()
