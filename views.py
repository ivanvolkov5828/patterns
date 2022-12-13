from render import render
from data.services import services
from data.users import users


def information_view(request):
    return '200 OK', render('index.html')


def services_view(request):
    return '200 OK', render('services.html', folder='templates', services=services)


def users_view(request):
    return '200 OK', render('users.html', folder='templates', users=users)
