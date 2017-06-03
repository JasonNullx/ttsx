# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from models import TypeInfo, GoodsInfo
from django.db.models import Count, Max
# Create your views here.


def index(request):
    type1_click = GoodsInfo.objects.filter(gtype_id=1).order_by('-gclick')[0:3]
    type1_new = GoodsInfo.objects.filter(gtype_id=1).order_by('-id')[0:4]
    type2_click = GoodsInfo.objects.filter(gtype_id=2).order_by('-gclick')[0:3]
    type2_new = GoodsInfo.objects.filter(gtype_id=2).order_by('-id')[0:4]
    type3_click = GoodsInfo.objects.filter(gtype_id=3).order_by('-gclick')[0:3]
    type3_new = GoodsInfo.objects.filter(gtype_id=3).order_by('-id')[0:4]
    type4_click = GoodsInfo.objects.filter(gtype_id=4).order_by('-gclick')[0:3]
    type4_new = GoodsInfo.objects.filter(gtype_id=4).order_by('-id')[0:4]
    type5_click = GoodsInfo.objects.filter(gtype_id=5).order_by('-gclick')[0:3]
    type5_new = GoodsInfo.objects.filter(gtype_id=5).order_by('-id')[0:4]
    type6_click = GoodsInfo.objects.filter(gtype_id=6).order_by('-gclick')[0:3]
    type6_new = GoodsInfo.objects.filter(gtype_id=6).order_by('-id')[0:4]

    context = {'title': '首页',
               'type1_click': type1_click,
               'type1_new': type1_new,
               'type2_click': type2_click,
               'type2_new': type2_new,
               'type3_click': type3_click,
               'type3_new': type3_new,
               'type4_click': type4_click,
               'type4_new': type4_new,
               'type5_click': type5_click,
               'type5_new': type5_new,
               'type6_click': type6_click,
               'type6_new': type6_new,
               }
    return render(request, 'goods/index.html', context)


def index2(request):
    click_new_list = []
    type_count = GoodsInfo.objects.aggregate(Max('gtype_id'))['gtype_id__max']
    for i in range(1, type_count+1):
        click = GoodsInfo.objects.filter(gtype_id=i).order_by('-gclick')[0:3]
        new = GoodsInfo.objects.filter(gtype_id=i).order_by('-id')[0:4]
        type_name = TypeInfo.objects.get(id=i)
        click_new_list.append([type_name, click, new])

    context = {'click_new_list': click_new_list}
    return render(request, 'goods/index.html', context)


def goods_list(request):
    return render(request, 'goods/list.html')


def goods_detail(request):
    return render(request, 'goods/detail.html')

