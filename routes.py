from views import information_view, services_view, users_view, contact_view, lst_of_courses, lst_of_categories, \
    create_a_course, create_a_category, copy_course

routes = {
    '/': information_view,
    '/services/': services_view,
    '/users/': users_view,
    '/contacts/': contact_view,

    # -------------------------
    # models.py

    # courses
    '/courses/': lst_of_courses,
    '/create-course/': create_a_course,

    # categories
    '/categories/': lst_of_categories,
    '/create-category/': create_a_category,

    # copy-course
    '/copy-course/': copy_course
}
