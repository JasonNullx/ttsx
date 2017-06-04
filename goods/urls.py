# coding:utf-8
from django.conf.urls import url
import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^goods_list(?P<tid>\d+)_(?P<orderby>\d)_(?P<pindex>\d*)', views.goods_list, name='goods_list'),
    url(r'^^goods_detail', views.goods_detail, name='goods_detail'),
]
