from urllib.parse import unquote_plus

from flask import (
    Blueprint,
    redirect,
    request,
    url_for,
    render_template,
    make_response
)

from models.session import Session
from routes import (
    NikuTemplate,
    current_user,
    html_response,
    random_string,
    redirect
)

from utils import log
from models.user import User


bp = Blueprint('routes_user', __name__)


@bp.route('/user/login', methods=['POST'])
def login():
    form = request.form

    u, result = User.login(form)
    if u.is_guest():
        return redirect(url_for('routes_user.login_view', result=result))
    else:
        session_id = random_string()
        form = dict(
            session_id=session_id,
            user_id=u.id,
        )
        Session.new(form)
        r = make_response(
            redirect(url_for('routes_user.login_view', result=result))
        )
        r.set_cookie("session_id", session_id)
        return r


@bp.route('/user/login/view')
def login_view():
    u = current_user()
    result = request.args.get('result', '')
    result = unquote_plus(result)

    return render_template(
        'login.html',
        username=u.username,
        result=result,
    )


@bp.route('/user/register', methods=['POST'])
def register():
    form = request.form.to_dict()
    u, result = User.register(form)

    return redirect(url_for('routes_user.register_view', result=result))


@bp.route('/user/register/view')
def register_view():
    result = request.args.get('result', '')
    result = unquote_plus(result)

    return render_template('register.html', result=result)
