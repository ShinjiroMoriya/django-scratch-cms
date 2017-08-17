from functools import wraps
from django.shortcuts import redirect


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.user.is_anonymous():
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper


def is_loginned(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        if request.user.is_authenticated():
            return redirect('/post')
        return func(*args, **kwargs)
    return wrapper
