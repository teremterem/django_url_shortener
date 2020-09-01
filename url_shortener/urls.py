from django.urls import path

from . import views

urlpatterns = [
    path('$', views.index, name='index'),
    path('shorten_url/$', views.shorten_url, name='shorten_url'),
    path('<str:url_handle>$', views.expand_url, name='expand_url'),
]
