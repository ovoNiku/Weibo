from utils import log

from flask import Flask
from routes.routes_public import bp as public
from routes.routes_user import bp as routes_user
from routes.api_weibo import bp as api_weibo
from routes.routes_weibo import bp as routes_weibo

app = Flask(__name__)
app.register_blueprint(public)
app.register_blueprint(routes_user)
app.register_blueprint(routes_weibo)
app.register_blueprint(api_weibo)

if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        debug=True,
        host='localhost',
        port=3000,
    )
    log('all url', app.url_map)
    app.run(**config)
