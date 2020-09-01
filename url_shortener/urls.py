from django.urls import path

from . import views

urlpatterns = [
    path('shorten_url/$', views.shorten_url, name='shorten_url'),
    path('', views.index, name='index'),
]
