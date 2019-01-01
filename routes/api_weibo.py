from flask import (
    Blueprint,
    request,
    redirect,
    jsonify,
)
# from functools import wraps
from utils import log
from routes import (
    json_response,
    current_user,
    weibo_owner_required,
    login_required,
    comment_owner_required,
)
from models.weibo import Weibo
from models.comment import Comment
from models.user import User

bp = Blueprint('api_weibo', __name__)


@bp.route('/api/weibo/all')
def all():
    weibos = Weibo.all_json()
    for weibo in weibos:
        id = weibo['id']
        user_id = weibo['user_id']
        cs = Comment.find_all(weibo_id=id)
        user = User.find_by(id=user_id)
        username = user.username
        list = []
        for i in range(len(cs)):
            cs_dict = {}
            comment = cs[i]
            u = comment.user()
            c = comment.json()
            c['username'] = u.username
            cs_dict.update(c)
            list.append(cs_dict)
        weibo['comment'] = list
        weibo['username'] = username
    return jsonify(weibos)


@bp.route('/api/weibo/add', methods=['POST'])
@login_required
def add():
    form = request.json
    u = current_user()
    w = Weibo.add(form, u.id).json()
    w['username'] = u.username
    return jsonify(w)


@bp.route('/api/weibo/delete')
@weibo_owner_required
@login_required
def delete():
    weibo_id = int(request.args['id'])
    Weibo.delete(weibo_id)
    cs = Comment.find_all(weibo_id=weibo_id)
    for c in cs:
        id = c.id
        Comment.delete(id)

    d = dict(
        message="成功删除 weibo"
    )
    return jsonify(d)


@bp.route('/api/weibo/update', methods=['POST'])
@weibo_owner_required
@login_required
def update():
    form = request.json
    weibo_id = int(form['id'])
    content = form['content']
    w = Weibo.update(weibo_id, content=content)
    return jsonify(w.json())


@bp.route('/api/weibo/comment', methods=['POST'])
@login_required
def comment_add():
    form = request.json
    u = current_user()
    c = Comment.add(form, u.id).json()
    c['username'] = u.username
    return jsonify(c)


@bp.route('/api/weibo/comment/delete')
@login_required
@comment_owner_required
def comment_delete():
    comment_id = int(request.args['id'])
    Comment.delete(comment_id)
    d = dict(
        message="成功删除 comment"
    )
    return jsonify(d)


@bp.route('/api/weibo/comment/update', methods=['POST'])
@comment_owner_required
@login_required
def comment_update():
    form = request.json
    comment_id = int(form['id'])
    content = form['content']
    c = Comment.update(comment_id, content=content)
    return jsonify(c.json())
