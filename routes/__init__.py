import os.path

from jinja2 import (
    Environment,
    FileSystemLoader,
)

from models.session import Session
from models.user import User
from utils import log
from models.comment import Comment
from models.weibo import Weibo

import random
import json
from functools import wraps

from flask import (
    request,
    redirect,
    url_for,
    jsonify,
)


def random_string():
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def initialized_environment():
    parent = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(parent, 'templates')
    loader = FileSystemLoader(path)
    e = Environment(loader=loader)
    return e


class NikuTemplate:
    e = initialized_environment()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        template = cls.e.get_template(filename)
        return template.render(*args, **kwargs)


def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        s = Session.find_by(session_id=session_id)
        if s is None or s.expired():
            return User.guest()
        else:
            user_id = s.user_id
            u = User.find_by(id=user_id)
            return u
    else:
        return User.guest()


def error(code=404):
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def formatted_header(headers, code=200):
    header = 'HTTP/1.1 {} OK GUA\r\n'.format(code)
    header += ''.join([
        '{}: {}\r\n'.format(k, v) for k, v in headers.items()
    ])
    return header


def html_response(body, headers=None):
    h = {
        'Content-Type': 'text/html',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_header(headers)
    r = header + '\r\n' + body
    return r.encode()


def json_response(data, headers=None):
    h = {
        'Content-Type': 'application/json',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)
    header = formatted_header(headers)
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body
    return r.encode()


def login_required(route_function):
    @wraps(route_function)
    def f():
        log('login_required')
        u = current_user()
        if u.is_guest():
            log('游客用户')
            return redirect(url_for('routes_user.login_view'))
        else:
            log('登录用户', route_function)
            return route_function()

    return f


def weibo_owner_required(route_function):
    @wraps(route_function)
    def f():
        u = current_user()
        if 'id' in request.args:
            weibo_id = int(request.args['id'])
            weibo = Weibo.find_by(id=weibo_id)
        else:
            form = request.json
            weibo_id = int(form['id'])
            weibo = Weibo.find_by(id=weibo_id)

        if weibo.user_id == u.id:
            log('pass 权限够')
            return route_function()
        else:
            log('权限不足')
            d = dict(
                message="权限不足",
            )
            return jsonify(d)

    return f


def comment_owner_required(route_function):
    @wraps(route_function)
    def f():
        u = current_user()
        if 'id' in request.args:
            comment_id = int(request.args['id'])
            comment = Comment.find_by(id=comment_id)
            weibo_id = comment.weibo_id
            weibo = Weibo.find_by(id=weibo_id)
        else:
            form = request.json
            weibo_id = int(form['id'])
            comment = Comment.find_by(id=weibo_id)
            weibo = Weibo.find_by(id=comment.weibo_id)

        if comment.user_id == u.id:
            log('pass 权限够')
            return route_function()
        elif weibo.user_id == u.id:
            log('pass 权限够')
            return route_function()
        else:
            log('权限不足')
            d = dict(
                message="权限不足",
            )
            return jsonify(d)

    return f
