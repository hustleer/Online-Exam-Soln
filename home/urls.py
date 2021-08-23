from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginpage, name='loginpage'),
    path('index', views.index, name='index'),
    path('postquestion', views.postquestion, name='postquestion'),
    path('imagepage', views.imagepage, name='imagepage'),
    path('refresh', views.refresh, name='refresh'),
    path('searchquestion', views.searchquestion, name='searchquestion'),
]
