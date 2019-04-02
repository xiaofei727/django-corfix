from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.index, name='login'),
    path('main', views.main, name='main'),
]