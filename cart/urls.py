# coding:utf-8
from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.cart_list, name='cart_list'),
    url(r'^add(?P<gid>\d+)_(?P<count>\d+)/$', views.add, name='add'),
    url(r'^cart_del/$', views.cart_del, name='cart_del'),
    url(r'^count_change/$', views.count_change, name='count_change'),
]
