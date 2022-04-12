from functools import wraps
from .response import drf_response
from rest_framework.response import Response
from django.contrib.auth import authenticate


def admin_logged(func):
    @wraps(func)
    def dec(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return drf_response(2)

        return func(request, *args, **kwargs)

    return dec


def user_logged(func):
    @wraps(func)
    def dec(request, *args, **kwargs):
        if 'openid' not in request.session:
            return drf_response(2)

        return func(request, *args, **kwargs)

    return dec
