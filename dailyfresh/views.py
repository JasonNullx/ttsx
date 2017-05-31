# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


# 写个装饰器，判断用户登录的状态
def logintest(func):
    pass


# # 主页视图
# @logintest
def index(request):
    # 判断用户是否登录
    user_id = request.session.get('user_id', None)
    if user_id is None:
        pass
    return render(request, 'index.html')

