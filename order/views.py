# coding:utf-8
from django.shortcuts import render
from users.user_verify import user_verify
from users.models import *
from cart.models import *

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

