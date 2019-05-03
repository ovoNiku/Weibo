from routes import (
    current_user,
    NikuTemplate,
    html_response,
)


def index(request):
    u = current_user(request)
    body = NikuTemplate.render('index.html', username=u.username)
    return html_response(body)


def static(request):
    filename = request.query['file']
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\n\r\n'
        img = header + f.read()
        return img


def route_dict():
    d = {
        '/': index,
        '/static': static,
    }
    return d
