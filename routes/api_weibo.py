from utils import log
from routes import json_response, current_user
from models.weibo import Weibo
from models.comment import Comment
from models.user import User
from models.session import Session


def all(request):
    weibos = Weibo.all_json()
    for weibo in weibos:
        log('weibo', weibo, type(weibo))
        id = weibo['id']
        user_id = weibo['user_id']
        user = User.one(id=user_id)
        username = user.username
        cs = Comment.all(weibo_id=id)
        for c in cs:
            c_user = User.one(id=c.user_id)
            c = c.__dict__
            c['username'] = c_user.username
        weibo['comment'] = cs
        weibo['username'] = username
    return json_response(weibos)


def add(request):
    form = request.json()
    u = current_user(request)
    w = Weibo.add(form, u.id).__dict__
    w['username'] = u.username
    return json_response(w)


def delete(request):
    weibo_id = int(request.query['id'])
    Weibo.delete(weibo_id)
    cs = Comment.all(weibo_id=weibo_id)
    for c in cs:
        id = c.id
        Comment.delete(id)

    d = dict(
        message="成功删除 weibo"
    )
    return json_response(d)


def update(request):
    form = request.json()
    weibo_id = int(form['id'])
    print('weibo_id', weibo_id)
    content = form['content']
    w = Weibo.update(weibo_id, content=content)
    return json_response(w.json())


def comment_add(request):
    form = request.json()
    u = current_user(request)
    c = Comment.add(form, u.id).__dict__
    c['username'] = u.username
    return json_response(c)


def comment_delete(request):
    comment_id = int(request.query['id'])
    Comment.delete(comment_id)
    d = dict(
        message="成功删除 comment"
    )
    return json_response(d)


def comment_update(request):
    form = request.json()
    comment_id = int(form['id'])
    content = form['content']
    c = Comment.update(comment_id, content=content)
    return json_response(c.json())


def owner_required(request):
    log('request.query')
    d = dict(
        message="权限不足",
    )
    return json_response(d)


def weibo_owner_required(route_function):
    def f(request):
        u = current_user(request)
        if 'id' in request.query:
            weibo_id = int(request.query['id'])
            weibo = Weibo.one(id=weibo_id)
        else:
            form = request.json()
            weibo_id = int(form['id'])
            weibo = Weibo.one(id=weibo_id)

        if weibo.user_id == u.id:
            log('pass 权限够')
            return route_function(request)
        else:
            log('权限不足')
            return owner_required(request)

    return f


def comment_owner_required(route_function):
    def f(request):
        u = current_user(request)
        if 'id' in request.query:
            comment_id = int(request.query['id'])
            comment = Comment.one(id=comment_id)
            weibo_id = comment.weibo_id
            weibo = Weibo.one(id=weibo_id)
        else:
            form = request.json()
            comment_id = int(form['id'])
            comment = Comment.one(id=comment_id)
            weibo_id = comment.weibo_id
            weibo = Weibo.one(id=weibo_id)

        if comment.user_id == u.id:
            log('pass 权限够')
            return route_function(request)
        elif weibo.user_id == u.id:
            log('pass 权限够')
            return route_function(request)
        else:
            log('权限不足')
            return owner_required(request)

    return f


def login_required(route_function):
    def f(request):
        u = current_user(request)
        if u.is_guest():
            return owner_required(request)
        else:
            return route_function(request)

    return f


def route_dict():
    d = {
        '/api/weibo/all': login_required(all),
        '/api/weibo/add': login_required(add),
        '/api/weibo/delete': weibo_owner_required(login_required(delete)),
        '/api/weibo/update':  weibo_owner_required(login_required(update)),
        '/api/weibo/comment': login_required(comment_add),
        '/api/weibo/comment/delete': comment_owner_required(login_required(comment_delete)),
        '/api/weibo/comment/update': comment_owner_required(login_required(comment_update)),
        '/api/weibo/owner': owner_required,
    }
    return d
