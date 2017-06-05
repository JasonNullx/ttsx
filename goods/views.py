# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from models import TypeInfo, GoodsInfo
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    list_model = []
    type_list = TypeInfo.objects.all()

    for type in type_list:
        try:
            click = GoodsInfo.objects.filter(gtype_id=type.id).order_by('-gclick')[0:3]
            new = GoodsInfo.objects.filter(gtype_id=type.id).order_by('-id')[0:4]
            type_name = type.ttitle
        except:
            continue
        banner_id = '0' + str(type.id) if type.id < 10 else str(type.id)

        list_model.append({'type_name': type_name,
                           'type_id': type.id,
                           'click': click,
                           'new': new,
                           'banner_id': banner_id,
                           })

    context = {'title': '首页', 'list_model': list_model}
    return render(request, 'goods/index.html', context)


def goods_list(request, tid, orderby, pindex,):
    # 如果匹配不到则pindex设为1
    if pindex == '':
        pindex = 1
    else:   # 注意正则匹配到的是字符串
        pindex = int(pindex)

    if orderby == '':
        orderby = 1
    else:
        orderby = int(orderby)

    # 获取某个类别下的所有商品
    goods = GoodsInfo.objects.filter(gtype_id=tid)

    # 排序
    if orderby == 1:
        goods = goods.order_by('-id')
    elif orderby == 2:
        goods = goods.order_by('gprice')
    else:
        goods = goods.order_by('-gclick')

    # 获取某个类别下的最新商品
    new_goods = goods.order_by('-id')[0:2]

    # 生成paginator对象
    paginator = Paginator(goods, 10)
    # 获取页码列表
    page_range = paginator.page_range
    # 获取最大页码
    num_pages = paginator.num_pages

    # 如果pindex大于最大页数，则pindex就等于最大页数
    if pindex > num_pages:
        pindex = num_pages

    # 获取某页的数据
    page = paginator.page(pindex)

    context = {'title': '列表页',
               'page': page,
               'new_goods': new_goods,
               'tid': tid,
               'page_range': page_range,
               'num_pages': num_pages,
               'orderby': orderby,
               }
    return render(request, 'goods/list.html', context)


def goods_detail(request, gid):
    good = GoodsInfo.objects.get(id=gid)
    good.gclick += 1
    good.save()
    new_goods = GoodsInfo.objects.filter(gtype_id=good.gtype_id).order_by('-id')[0:2]

    context = {'title': '详情页',
               'new_goods': new_goods,
               'good': good,
               }
    return render(request, 'goods/detail.html', context)

