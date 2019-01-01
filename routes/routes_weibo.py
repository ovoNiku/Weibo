from functools import wraps

from flask import (
    Blueprint,
    request,
    render_template,
)

from models.weibo import Weibo
from routes import (
    redirect,
    NikuTemplate,
    current_user,
    html_response,
    login_required,
)
from utils import log

bp = Blueprint('routes_weibo', __name__)


@bp.route('/weibo/index')
@login_required
def index():
    """
    weibo 首页的路由函数
    """
    return render_template('weibo_index.html')


def same_user_required(route_function):
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    @wraps(route_function)
    def f():
        u = current_user()
        if 'id' in request.args:
            weibo_id = request.args['id']
        else:
            weibo_id = request.form['id']
        t = Weibo.find_by(id=int(weibo_id))

        if t.user_id == u.id:
            return route_function()
        else:
            return redirect('/weibo/index')

    return f


