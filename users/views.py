# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from models import Users
import hashlib
from user_verify import user_verify

# Create your views here.


def register(request):
    context = {'title': '用户注册'}
    return render(request, 'users/register.html', context)


def register_handle(request):
    if request.method == 'POST':
        # 获取post数据
        post_data = request.POST

        # 如果post没有数据，则跳回注册页
        if not len(post_data):
            return redirect('/register')

        uname = post_data.get('username')
        upass = post_data.get('pwd')
        cpwd = post_data.get('cpwd')
        email = post_data.get('email')

        # 判断注册的用户是否存在     ---> 回头可以改成ajax，就省去跳转到另一个页面再跳回来了
        # user_exist = Users.objects.filter(uname=uname)
        # if user_exist:
        #     info = "用户已经存在!"
        #     re_url = "/register"
        #     context = {'info': info, 're_url': re_url}
        #     return render(request, 'users/redirect.html', context)

        # 若两次输入的密码一致，则添加至数据库
        if upass == cpwd:
            m = hashlib.md5()
            m.update(upass)
            md5_upass = m.hexdigest()

            Users.objects.create(uname=uname, upass=md5_upass, email=email)

            # 注册成功，跳转至登录界面
            return redirect('/login')
    else:
        return redirect('/register')


def register_exist(request):
    uname = request.GET.get('uname')
    count = Users.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    context = {'title': '用户登录'}
    return render(request, 'users/login.html', context)


def login_handle(request):
    if request.method == 'POST':
        post_data = request.POST
        uname = post_data.get('username')
        upass = post_data.get('pwd')

        # 如果post没有数据，则跳回login页
        if not len(post_data):
            return redirect('/login')

        user_exist = Users.objects.filter(uname=uname)
        if not user_exist:
            info = "用户不存在!"
            re_url = "/login"
            context = {'info': info, 're_url': re_url}
            return render(request, 'users/redirect.html', context)

        m = hashlib.md5()
        m.update(upass)
        md5_upass = m.hexdigest()

        if md5_upass == user_exist[0].upass:
            request.session['user_id'] = user_exist[0].id
            request.session['user_name'] = user_exist[0].uname
            # 登录成功，进行跳转
            # 根据cookie中的url字段判断用户是从哪个页面跳到登录页面的，从而跳转那个页面
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)
            red.set_cookie('url', '', max_age=-1)
            return red
        else:
            # 密码错误的情况
            info = "密码错误!"
            re_url = "/login"
            context = {'info': info, 're_url': re_url}
            return render(request, 'users/redirect.html', context)
    else:
        return redirect('/login')


def logout(request):
    request.session.flush()
    red = HttpResponseRedirect('/')
    return red


@user_verify
def user_center_info(request):
    context = {'active': 'info', 'title': '个人信息'}
    return render(request, 'users/user_center_info.html', context)


@user_verify
def user_center_order(request):
    context = {'active': 'order', 'title': '订单'}
    return render(request, 'users/user_center_order.html', context)


@user_verify
def user_center_site(request):
    context = {'active': 'site', 'title': '收获地址'}
    return render(request, 'users/user_center_site.html', context)
