from django.conf.urls import url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from hacku import views

urlpatterns = [
    url(r'^start/$', csrf_exempt(views.start), name='start'),
    url(r'^refresh/$', views.refresh, name='refresh'),
    # url(r'^photo/$', views.photo, name='photo')
]