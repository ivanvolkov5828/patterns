from routes import routes
from waitress import serve
from dependencies import get_request_params, decode_value, post_get_request_params

def user_controller(request):
    request['users'] = {
        'first_name': 'Ivan',
        'last_name': 'Volkov',
        'age': 20
    }


front_controllers = [user_controller]


def application(environ, start_response, routes: dict = routes, front_controllers: list = front_controllers):
    path = environ['PATH_INFO']

    if not path.endswith('/'):
        path = f'{path}/'

    request = {}
    method = environ['REQUEST_METHOD']
    request['method'] = method

    if method == 'POST':
        data = post_get_request_params(environ)
        request['data'] = decode_value(data)
        print(f'POST-запрос: {decode_value(data)}')

    if method == 'GET':
        request_params = get_request_params(environ)
        request['request_params'] = decode_value(request_params)
        print(f'GET-запрос: {decode_value(request_params)}')

    if path in routes:
        view = routes[path]

        for controller in front_controllers:
            controller(request)

        code, text = view(request)

        start_response(code, [('Content-Type', 'text/html')])

        return [text.encode('utf-8')]

    else:
        start_response('404 PAGE NOT FOUND', [('Content-Type', 'text/html')])
        return [b"Page not found!"]


if __name__ == '__main__':
    serve(application, listen='0.0.0.0:8000')
