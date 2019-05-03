from models.comment import Comment
from routes import json_response, current_user
from models.weibo import Weibo
from routes import (
    redirect,
    NikuTemplate,
    current_user,
    html_response,
)
from utils import log


def index(request):
    body = NikuTemplate.render('weibo_index.html')
    return html_response(body)


def index_test(request):
    body = NikuTemplate.render('weibo_index_test.html')
    return html_response(body)


def owner_required(request):
    log('request.query')
    d = dict(
        message="权限不足",
    )
    return json_response(d)


def login_required(route_function):
    def f(request):
        u = current_user(request)
        if u.is_guest():
            return index_test(request)
        else:
            return route_function(request)

    return f


def route_dict():
    d = {
        '/weibo/index': login_required(index),
    }
    return d
