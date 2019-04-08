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
    return render_template('weibo_index.html')


def same_user_required(route_function):
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


