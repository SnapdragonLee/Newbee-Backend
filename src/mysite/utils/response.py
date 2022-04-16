from rest_framework.response import Response


def drf_response(ret, msg='', **data):
    if ret == 0:
        data["ret"] = 0
        data["msg"] = msg
        return Response(data=data, status=200)
    elif ret == 1:
        return Response(data={"ret": 1, "msg": "User is not logged in"}, status=200)
    elif ret == 2:
        return Response(data={"ret": 2, "msg": "Administrator is not logged in"}, status=200)
    elif ret == 3:
        data["ret"] = 3
        data["msg"] = msg
        return Response(data=data, status=200)
