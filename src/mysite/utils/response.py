from rest_framework.response import Response


def drf_response(ret, **data):
    if ret == 0:
        return Response(data={"ret": 0, "msg": "admin login success"}, status=200)
    elif ret == 1:
        return Response(data={"ret": 1, "msg": "No user find in admin db"}, status=200)
    elif ret == 2:
        return Response(data={"ret": 2, "msg": "No user find in user db"}, status=200)
