import datetime
import os.path

from render import render
from data.services import services
from data.users import users


def information_view(request):
    return '200 OK', render('index.html')


def services_view(request):
    return '200 OK', render('services.html', folder='templates', services=services)


def users_view(request):
    return '200 OK', render('users.html', folder='templates', users=users)


def contact_view(request):
    if request['method'] == 'POST':
        now = datetime.datetime.now()
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']

        if not os.path.exists('messages'):
            os.mkdir('messages')

        with open(f'messages/message_{now.strftime("%d%m%Y")}_{now.strftime("%H%M%S")}.txt', 'w',
                      encoding='utf-8') as file:
            file.write(f'Нам пришло сообщение от {now.strftime("%d.%m.%Y")} в {now.strftime("%H:%M:%S")}!\n'
                           f'Отправитель: {email}\n'
                           f'Тема: {title}\n'
                           f'Текст: {text}')
        return '200 OK', render('contacts.html')
    else:
        return '200 OK', render('contacts.html')
