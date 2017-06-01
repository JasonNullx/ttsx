# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from users.models import Users
# Create your views here.


# # 主页视图
# @user_verify
def index(request):
    # 判断用户是否登录
    context = {'title': '首页'}
    user_id = request.session.get('user_id', None)
    if user_id is None:
        context['logined'] = False
        return render(request, 'index.html', context)
    else:
        uname = Users.objects.get(id=int(user_id)).uname
        context['logined'] = True
        context['uname'] = uname
        return render(request, 'index.html', context)

