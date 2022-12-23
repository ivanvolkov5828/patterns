import datetime
import os.path

from render import render
from data.services import services
from data.users import users

from models import Engine, Logger

site = Engine()
logger = Logger('main')


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


# ----------------------------------------------------------------------------------------------------------------------
# Контроллеры для созданных моделей в файле models.py

# 1: list_of_categories
def lst_of_categories(request):
    logger.log('Список категорий')
    return '200 OK', render('categories.html', folder='templates', categories=site.categories)


# 2: list_of_courses
def lst_of_courses(request):
    logger.log('Список курсов')
    try:
        category = site.find_category_by_id(int(request['request_params']['id']))
        return '200 OK', render('courses.html', folder='templates',
                                courses=category.courses, name=category.name,
                                id=category.id)
    except KeyError:
        return '200 OK', 'No courses have been added yet'


# 3: create_a_course
def create_a_course(request):
    category_id = -1

    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        name = site.decode_value(name)

        category = None
        if category_id != -1:
            category = site.find_category_by_id(int(category_id))
            corse = site.create_course('record', name, category)
            site.courses.append(corse)

        return '200 OK', render('courses.html', folder='templates',
                                courses=category.courses, name=category.name,
                                id=category.id)
    else:
        try:
            category_id = int(request['request_params']['id'])
            category = site.find_category_by_id(int(category_id))

            return '200 OK', render('create_course.html', folder='templates',
                                    name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No categories have been added yet'


# 4: create a category
def create_a_category(request):
    if request['method'] == 'POST':

        data = request['data']

        name = data['name']
        name = site.decode_value(name)

        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)

        site.categories.append(new_category)

        return '200 OK', render('categories.html', folder='templates', categories=site.categories)
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', folder='templates',
                                categories=categories)


# 5: copy_course
def copy_course(request):
    request_params = request['request_params']

    try:
        name = request_params['name']

        old_course = site.get_course(name)
        if old_course:
            new_name = f'copy_{name}'
            new_course = old_course.clone()
            new_course.name = new_name
            site.courses.append(new_course)

        return '200 OK', render('courses.html', folder='templates',
                                courses=site.courses,
                                name=new_course.category.name)

    except KeyError:
        return '200 OK', 'No courses have been added yet'
