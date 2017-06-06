# coding:utf-8
from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.cart_list, name='cart_list'),
    url(r'^add(?P<gid>\d+)_(?P<count>\d+)/$', views.add, name='add'),

]
