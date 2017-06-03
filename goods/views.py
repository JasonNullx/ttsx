# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from models import TypeInfo, GoodsInfo
# Create your views here.


def index(request):
    type1_click = GoodsInfo.objects.filter(gtype_id=1).order_by('-gclick')[0:3]
    type1_new = GoodsInfo.objects.filter(gtype_id=1).order_by('-id')[0:4]
    context = {'title': '首页',
               'type1_click': type1_click,
               'type1_new': type1_new,
               }
    return render(request, 'goods/index.html', context)


def goods_list(request):
    return render(request, 'goods/list.html')


def goods_detail(request):
    return render(request, 'goods/detail.html')

