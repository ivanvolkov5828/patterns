from views import information_view, services_view, users_view, contact_view

routes = {
    '/': information_view,
    '/services/': services_view,
    '/users/': users_view,
    '/contacts/': contact_view,
}
