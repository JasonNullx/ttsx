# coding:utf-8
from django.conf.urls import url
import views


urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^register_action/$', views.register_action, name='register_action'),
]
