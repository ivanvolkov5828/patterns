import datetime
import os.path

from functions.render import render
from data.services import services
from data.users import users

from patterns.models import Engine, Logger
from patterns.app_route import AppRoute
from patterns.debug import Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, \
    TemplateView, ListVIew, CreateView, \
    BaseSerializer, ConsoleWriter, FileWriter

site = Engine()
logger = Logger('main', ConsoleWriter())
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

routes = {}

# @AppRoute(routes=routes, url='/')
# @Debug(name='Index')
# def information_view(request):
#     return '200 OK', render('index.html')


@AppRoute(routes=routes, url='/')
class InformationView:
    @Debug(name='InformationView')
    def __call__(self, request):
        return '200 OK', render('index.html')


# @AppRoute(routes=routes, url='/services/')
# @Debug(name='Services')
# def services_view(request):
#     return '200 OK', render('services.html', folder='templates', services=services)


@AppRoute(routes=routes, url='/services/')
class ServicesView:
    @Debug(name='ServicesView')
    def __call__(self, request):
        return '200 OK', render('services.html', folder='templates', services=services)


# @AppRoute(routes=routes, url='/users/')
# @Debug(name='Users')
# def users_view(request):
#     return '200 OK', render('users.html', folder='templates', users=users)


@AppRoute(routes=routes, url='/users/')
class UsersView:
    @Debug(name='UsersView')
    def __call__(self, request):
        return '200 OK', render('users.html', folder='templates', users=users)


# @AppRoute(routes=routes, url='/contacts/')
# @Debug(name='Contacts')
# def contact_view(request):
#     if request['method'] == 'POST':
#         now = datetime.datetime.now()
#         data = request['data']
#         title = data['title']
#         text = data['text']
#         email = data['email']
#
#         if not os.path.exists('messages'):
#             os.mkdir('messages')
#
#         with open(f'messages/message_{now.strftime("%d%m%Y")}_{now.strftime("%H%M%S")}.txt', 'w',
#                   encoding='utf-8') as file:
#             file.write(f'Нам пришло сообщение от {now.strftime("%d.%m.%Y")} в {now.strftime("%H:%M:%S")}!\n'
#                        f'Отправитель: {email}\n'
#                        f'Тема: {title}\n'
#                        f'Текст: {text}')
#         return '200 OK', render('contacts.html')
#     else:
#         return '200 OK', render('contacts.html')


@AppRoute(routes=routes, url='/contacts/')
class ContactsView:
    @Debug(name='ContactsView')
    def __call__(self, request):
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
# @AppRoute(routes=routes, url='/categories/')
# @Debug(name='Categories')
# def lst_of_categories(request):
#     logger.log('Список категорий')
#     return '200 OK', render('categories.html', folder='templates', categories=site.categories)


@AppRoute(routes=routes, url='/categories/')
class LstOfCategoriesView:
    @Debug(name='LstOfCategoriesView')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('categories.html', folder='templates', categories=site.categories)


# 2: list_of_courses
# @AppRoute(routes=routes, url='/courses/')
# @Debug(name='Courses')
# def lst_of_courses(request):
#     logger.log('Список курсов')
#     try:
#         category = site.find_category_by_id(int(request['request_params']['id']))
#         return '200 OK', render('courses.html', folder='templates',
#                                 courses=category.courses, name=category.name,
#                                 id=category.id)
#     except KeyError:
#         return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/courses/')
class LstOfCoursesView:
    @Debug(name='LstOfCoursesView')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('courses.html', folder='templates',
                                    courses=category.courses, name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# 3: create_a_course
# @AppRoute(routes=routes, url='/create-course/')
# def create_a_course(request):
#     category_id = -1
#
#     if request['method'] == 'POST':
#         data = request['data']
#         name = data['name']
#         name = site.decode_value(name)
#
#         category = None
#         if category_id != -1:
#             category = site.find_category_by_id(int(category_id))
#             corse = site.create_course('record', name, category)
#             site.courses.append(corse)
#
#         return '200 OK', render('courses.html', folder='templates',
#                                 courses=category.courses, name=category.name,
#                                 id=category.id)
#     else:
#         try:
#             category_id = int(request['request_params']['id'])
#             category = site.find_category_by_id(int(category_id))
#
#             return '200 OK', render('create_course.html', folder='templates',
#                                     name=category.name,
#                                     id=category.id)
#         except KeyError:
#             return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/create-course/')
class CreateACourseView:
    category_id = -1
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)

                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)

                site.courses.append(course)

            return '200 OK', render('courses.html', folder='templates',
                                    courses=category.courses, name=category.name,
                                    id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', folder='templates',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# 4: create_a_category
# @AppRoute(routes=routes, url='/create-category/')
# def create_a_category(request):
#     if request['method'] == 'POST':
#
#         data = request['data']
#
#         name = data['name']
#         name = site.decode_value(name)
#
#         category_id = data.get('category_id')
#
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#
#         new_category = site.create_category(name, category)
#
#         site.categories.append(new_category)
#
#         return '200 OK', render('categories.html', folder='templates', categories=site.categories)
#     else:
#         categories = site.categories
#         return '200 OK', render('create_category.html', folder='templates',
#                                 categories=categories)


@AppRoute(routes=routes, url='/create-category/')
class CreateACategoryView:
    def __call__(self, request):
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
# @AppRoute(routes=routes, url='/copy-course/')
# def copy_course(request):
#     request_params = request['request_params']
#
#     try:
#         name = request_params['name']
#
#         old_course = site.get_course(name)
#         if old_course:
#             new_name = f'copy_{name}'
#             new_course = old_course.clone()
#             new_course.name = new_name
#             site.courses.append(new_course)
#
#         return '200 OK', render('courses.html', folder='templates',
#                                 courses=site.courses,
#                                 name=new_course.category.name)
#
#     except KeyError:
#         return '200 OK', 'No courses have been added yet'


@AppRoute(routes=routes, url='/copy-course/')
class CopyCoursesView:
    def __call__(self, request):
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
# ----------------------------------------------------------------------------------------------------------------------
# inheritance

@AppRoute(routes=routes,  url='/student-list/')
class StudentListView(ListVIew):
    queryset = site.students
    template_name = 'student_list.html'


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)


@AppRoute(routes=routes, url='/api/')
class CourseApi:
    @Debug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()

