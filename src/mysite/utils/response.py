from rest_framework.response import Response


def drf_response(ret, **data):
    if ret == 0:
        data['ret'] = '0'
        return Response(data=data, status=200)
    elif ret == 1:
        return Response(data={"ret": '1'}, status=200)
    elif ret == 2:
        return Response(data={"ret": '2'}, status=200)
