# coding:utf-8
from django.shortcuts import render
from users.user_verify import user_verify
# Create your views here.


@user_verify
def cart(request):
    context = {'title': '购物车'}
    return render(request, 'cart/cart.html', context)


