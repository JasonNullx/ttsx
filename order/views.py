# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.user_verify import user_verify
from order.models import *
from cart.models import *
from datetime import datetime
from django.db import transaction

# Create your views here.


@user_verify
def order_list(request):
    user_info = Users.objects.filter(id=request.session['user_id'])

    cart_id_list = request.GET.getlist('cart_id')
    cart_list = CartInfo.objects.filter(id__in=cart_id_list)

    context = {'title': '提交订单',
               'user_info': user_info[0],
               'cart_list': cart_list,
               }
    return render(request, 'order/place_order.html', context)


'''
提交订单功能：
1、判断库存
2、减少库存
3、创建订单对象
4、创建详单对象
5、删除购物车
对于以上操作，应该使用事务

未实现功能：
    真实支付
    物流跟踪
'''


@transaction.atomic
@user_verify
def order_sub(request):
    cart_id_list = request.POST.getlist('cart_id')
    oaddress = request.POST.get('address')
    if not cart_id_list or not oaddress:
        return redirect('/cart/')

    now = datetime.now()
    user_id = request.session['user_id']
    oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), user_id)

    # 创建事务的保存点
    sid = transaction.savepoint()
    try:
        # 创建订单对象
        order = OrderInfo()
        order.oid = oid
        order.odate = now
        order.oaddress = oaddress
        order.user_id = user_id
        order.ototal = 0
        order.save()

        # 遍历cart
        for cart_id in cart_id_list:
            cart = CartInfo.objects.filter(id=cart_id)
            if cart:
                cart = cart[0]
                # 判断库存
                if cart.count <= cart.goods.gkucun:
                    # 减少库存
                    cart.goods.gkucun -= cart.count
                    cart.goods.save()

                    # 计算总价
                    price = cart.goods.gprice
                    count = cart.count
                    total = float('%.2f' % (price * count))
                    order.ototal += total
                    # 创建详单对象
                    detailinfo = OrderDetailInfo()
                    detailinfo.price = price
                    detailinfo.count = count
                    detailinfo.goods = cart.goods
                    detailinfo.order = order
                    detailinfo.save()

                    # 删除购物车
                    cart.delete()
                else:
                    # 库存不够
                    transaction.savepoint_rollback(sid)
                    return redirect('/cart/')

        order.save()
        transaction.savepoint_commit(sid)
        return redirect('/users/user_center_order/')
    except Exception, e:
        print e
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')


def pay_order(request, oid):
    order = OrderInfo.objects.filter(oid=oid)
    if order:
        order = order[0]
        order.oIsPay = True
        order.save()

    return redirect('/users/user_center_order/')
