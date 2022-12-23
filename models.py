from copy import deepcopy
from quopri import decodestring


# PROTOTYPE
# ----------------------------------------------------------------------------------------------------------------------
class PrototypeMixin:
    def clone(self):
        return deepcopy(self)


# ----------------------------------------------------------------------------------------------------------------------


# USERS
# ----------------------------------------------------------------------------------------------------------------------
class User:
    pass


class Teacher(User):
    pass


class Student(User):
    pass


# FACTORY
class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()
# ----------------------------------------------------------------------------------------------------------------------


# CATEGORIES
# ----------------------------------------------------------------------------------------------------------------------
class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        res = len(self.courses)
        if self.category:
            res += self.category.course_count()
        return res
# ----------------------------------------------------------------------------------------------------------------------


# COURSES
# ----------------------------------------------------------------------------------------------------------------------
class Course(PrototypeMixin):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


# FACTORY
class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)
# ----------------------------------------------------------------------------------------------------------------------


# SINGLETON
# ----------------------------------------------------------------------------------------------------------------------
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]
# ----------------------------------------------------------------------------------------------------------------------


# Logger
# ----------------------------------------------------------------------------------------------------------------------
class Logger(metaclass=SingletonByName):
    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
# ----------------------------------------------------------------------------------------------------------------------


# CORE
# ----------------------------------------------------------------------------------------------------------------------
class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')

    def find_category_by_id(self, id):
        for category in self.categories:
            if category.id == id:
                return category
            else:
                raise Exception(f'Категории с id = {id} не существует')

    def get_course(self, name):
        for course in self.courses:
            if course.name == name:
                return course
            else:
                raise Exception(f'Такого курса не существует')
# ----------------------------------------------------------------------------------------------------------------------
