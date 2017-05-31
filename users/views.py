# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from models import Users
import hashlib

# Create your views here.


def register(request):
    return render(request, 'users/register.html')


def register_handle(request):
    # 获取post数据
    post_data = request.POST

    # 如果post没有数据，则跳回注册页
    if not len(post_data):
        return redirect('/users/register')

    uname = post_data.get('username')
    upass = post_data.get('pwd')
    cpwd = post_data.get('cpwd')
    email = post_data.get('email')

    # 判断注册的用户是否存在
    user_exist = Users.objects.filter(uname=uname)
    if user_exist:
        info = "用户已经存在!"
        re_url = "/register"
        context = {'info': info, 're_url': re_url}
        return render(request, 'users/redirect.html', context)

    # 若两次输入的密码一致，则添加至数据库
    if upass == cpwd:
        m = hashlib.md5()
        m.update(upass)
        md5_upass = m.hexdigest()

        Users.objects.create(uname=uname, upass=md5_upass, email=email)

        info = "注册成功!"
        re_url = "/"
        context = {'info': info, 're_url': re_url}
        return render(request, 'users/redirect.html', context)


def login(request):
    return render(request, 'users/login.html')


def login_handle(request):
    post_data = request.POST


def user_center(request):
    pass
