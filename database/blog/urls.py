from django.contrib import admin
from django.urls import path,include
import blog.views

urlpatterns = [
    path('', blog.views.show_login),
    path('login', blog.views.login, name = 'check'),
    path('register', blog.views.register, name = 'check2'),
    path('index', blog.views.index),
    path('detail/<int:article_id>', blog.views.get_detail_page),
    path('edit', blog.views.edit, name = 'check3'),
    path('person_info', blog.views.person_info),
    path('insert', blog.views.insert, name = 'check4'),
    path('show_insert', blog.views.show_insert),
    path('delete', blog.views.delete, name = 'check5')
]
