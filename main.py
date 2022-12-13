from routes import routes
from waitress import serve


def user_controller(request):
    request['users'] = {
        'first_name': 'Ivan',
        'last_name': 'Volkov',
        'age': 20
    }


front_controllers = [user_controller]


def application(environ, start_response, routes: dict = routes, front_controllers: list = front_controllers):
    path = environ['REQUEST_URI']

    if path in routes:
        view = routes[path]
        request = {}

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
