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
    """
    生成一个随机的字符串
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        # 因为不确定边界这里就直接 len(seed) - 2
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def initialized_environment():
    parent = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(parent, 'templates')
    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(path)
    # 用加载器创建一个环境, 有了它才能读取模板文件
    e = Environment(loader=loader)
    return e


class NikuTemplate:
    e = initialized_environment()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        # 调用 get_template() 方法加载模板并返回
        template = cls.e.get_template(filename)
        # 用 render() 方法渲染模板
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
    """
    根据 code 返回不同的错误响应
    """
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
    """
    返回 json 格式的 body 数据
    前端的 ajax 函数就可以用 JSON.parse 解析出格式化的数据
    """
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
    # 登录权限，判断是否为游客
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
    # 判断是否为同一weibo用户
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
    # 判断是否为同一评论用户或该微博的user
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
