from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginpage, name='loginpage'),
    path('index', views.index, name='index'),
    path('postquestion', views.postquestion, name='postquestion'),
    path('searchquestion', views.searchquestion, name='searchquestion'),
]