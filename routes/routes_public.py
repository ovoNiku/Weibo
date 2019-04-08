from flask import (
    Blueprint,
    render_template,
)

from routes import (
    current_user,
)

bp = Blueprint('public', __name__)


@bp.route('/')
def index():
    u = current_user()
    return render_template('index.html', username=u.username)
