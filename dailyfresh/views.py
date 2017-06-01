# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from users.models import Users
# Create your views here.


def index(request):
    # 判断用户是否登录
    context = {'title': '首页'}
    return render(request, 'index.html', context)

