# import the url from django
from django.urls import path
# import the view module/file
from . import views


# make a list to connects the url/paths to a specific views
urlpatterns = [
    # '' -> root/base url of website
    path('', views.main, name='main'),

    # auth
    path('auth/register', views.register, name='register',),
    path('me/profile', views.profile, name='profile',),

    # retrive all books or create a book if post req
    path('books', views.books, name='get_books'),
    # alter or delete a book
    path('books/<int:pk>', views.book, name='book_alter')
]

# ALSO CONNECT FORM MAIN APP.
