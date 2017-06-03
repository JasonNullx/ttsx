# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from models import TypeInfo, GoodsInfo
from django.db.models import Count, Max
# Create your views here.


def index(request):
    list_model = []
    type_count = TypeInfo.objects.aggregate(Count('id'))['id__count']

    for i in range(1, type_count+1):
        try:
            click = GoodsInfo.objects.filter(gtype_id=i).order_by('-gclick')[0:3]
            new = GoodsInfo.objects.filter(gtype_id=i).order_by('-id')[0:4]
            type_name = TypeInfo.objects.get(id=i)
        except:
            continue

        banner_id = '0' + str(i) if i < 10 else str(i)
        list_model.append({'type_name': type_name,
                           'click': click,
                           'new': new,
                           'banner_id': banner_id,
                           })

    context = {'title': '首页', 'list_model': list_model}
    return render(request, 'goods/index.html', context)


def goods_list(request):
    return render(request, 'goods/list.html')


def goods_detail(request):
    return render(request, 'goods/detail.html')

