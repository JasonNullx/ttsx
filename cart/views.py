# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from users.user_verify import user_verify
from models import CartInfo
# Create your views here.


@user_verify
def add(request, gid, count):
    carts = CartInfo.objects.filter(goods_id=gid).filter(user_id=request.session['user_id'])
    # 如果添加的商品已经在用户的购物车，则只要增加该商品的数量即可，不用再增加一条记录了
    if len(carts) == 0:
        cart = CartInfo()
        cart.goods_id = int(gid)
        cart.user_id = request.session['user_id']
        cart.count = int(count)
        cart.save()
    else:
        cart = carts[0]
        cart.count += int(count)
        cart.save()

    # 判断是否是ajax请求，如果是ajax请求，则返回json对象
    if request.is_ajax():
        # 查询用户购物车中的商品数量
        show_count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count': show_count, 'is_login': 1})
    else:
        return redirect('/cart/')


@user_verify
def cart_list(request):
    cart_li = CartInfo.objects.filter(user_id=request.session['user_id'])
    context = {'title': '购物车',
               'page_name': 1,
               'cart_li': cart_li,
               }
    return render(request, 'cart/cart.html', context)


@user_verify
def cart_del(request):
    cid = int(request.GET['id'])
    cart_item = CartInfo.objects.filter(id=cid)
    is_del = 0
    if cart_item:
        try:
            cart_item.delete()
            is_del = 1
        except:
            is_del = 0

    return JsonResponse({'is_del': is_del})


@user_verify
def count_change(request):
    cid = request.GET['id']
    count = int(request.GET['count'])
    is_change = 0

    cart = CartInfo.objects.filter(id=cid)

    if cart:
        cart = cart[0]
        if count > cart.goods.gkucun:   # 输入的数量大于库存
            cart.count = cart.goods.gkucun
            cart.save()
        else:
            cart.count = count
            cart.save()

        is_change = 1

    return JsonResponse({'is_change': is_change})



