# coding:utf-8
from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index2/$', views.index2, name='index2$'),
    url(r'^goods_list', views.goods_list, name='goods_list'),
    url(r'^^goods_detail', views.goods_detail, name='goods_detail'),
]
