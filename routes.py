from views import information_view, services_view, users_view

routes = {
    '/': information_view,
    '/services': services_view,
    '/users': users_view,
}
