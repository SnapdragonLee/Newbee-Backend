from functools import wraps
from .response import wrap_response_data
from django.http import JsonResponse


def admin_logged(func):
    @wraps(func)
    def dec(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(data=wrap_response_data(2))

        print(request.user.username)
        return func(request, *args, **kwargs)

    return dec


def user_logged(func):
    @wraps(func)
    def dec(request, *args, **kwargs):
        if 'openid' not in request.session:
            return JsonResponse(data=wrap_response_data(1))

        return func(request, *args, **kwargs)

    return dec
