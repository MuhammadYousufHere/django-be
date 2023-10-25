# import the url from django
from django.urls import path
# import the view module/file
from . import views


# make a list to connects the url/paths to a specific views
urlpatterns = [
    # '' -> root/base url of website
    path('', views.main, name='upload'),

    # auth
    path('auth/register', views.register, name='register',),
    path('me/profile', views.profile, name='profile',),
    # path('api/sign_up/', views.SignUpView.as_view(), name='sign_up'),
    # path('api/log_in/', views.LogInView.as_view(), name='log_in'),
    # retrive all books or create a book if post req
    path('books', views.books, name='get_books'),
    # alter or delete a book
    path('books/<int:pk>', views.book, name='book_alter')
]

# ALSO CONNECT FORM MAIN APP.
