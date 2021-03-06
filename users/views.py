# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from models import Users
from goods.models import GoodsInfo
from order.models import OrderInfo, OrderDetailInfo
import hashlib
from user_verify import user_verify
from django.core.paginator import Paginator
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
            return redirect('/users/register')

        uname = post_data.get('username')
        upass = post_data.get('pwd')
        cpwd = post_data.get('cpwd')
        email = post_data.get('email')

        # 判断用户名是否存在
        if Users.objects.filter(uname=uname):
            return redirect('/users/register')

        # 若两次输入的密码一致，则添加至数据库
        if upass == cpwd:
            m = hashlib.md5()
            m.update(upass)
            md5_upass = m.hexdigest()

            Users.objects.create(uname=uname, upass=md5_upass, email=email)

            # 注册成功，跳转至登录界面
            return redirect('/users/login')
    else:
        return redirect('/users/register')


def register_exist(request):
    uname = request.GET.get('uname')
    count = Users.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'users/login.html', context)


def login_handle(request):
    if request.method == 'POST':
        post_data = request.POST
        uname = post_data.get('username')
        upass = post_data.get('pwd')
        rem = post_data.get('remember')

        # 如果post没有数据，则跳回login页
        if not len(post_data):
            return redirect('/users/login')

        # 判断用户是否存在，不存在跳到登录页。前端虽然使用js进行了判断，这里再做一次是防止用户跳过js
        user_exist = Users.objects.filter(uname=uname)
        if user_exist:
            # 对用户输入的密码进行md5加密
            m = hashlib.md5()
            m.update(upass)
            md5_upass = m.hexdigest()

            if md5_upass == user_exist[0].upass:
                # 登录成功，会往服务器本地存储用户的session信息
                request.session['user_id'] = user_exist[0].id
                request.session['user_name'] = user_exist[0].uname

                # 根据cookie中的url字段判断用户是从哪个页面跳到登录页面的，从而跳转那个页面
                url = request.COOKIES.get('red_url', '/')
                red = redirect(url)
                red.set_cookie('red_url', '', max_age=-1)

                # 判断是否记住用户名
                if rem == '1':
                    red.set_cookie('uname', uname)
                else:
                    red.set_cookie('uname', '', max_age=-1)

                return red
            else:  # 密码错误
                context = {'title': '用户登录',
                           'error_name': 0,
                           'error_pwd': 1,
                           'uname': uname,
                           'upass': upass,
                           }
                return render(request, 'users/login.html', context)
        else:  # 用户不存在
            context = {'title': '用户登录',
                       'error_name': 1,
                       'error_pwd': 0,
                       'uname': uname,
                       'upass': upass,
                       }
            return render(request, 'users/login.html', context)
    else:
        return redirect('/users/login')


def logout(request):
    request.session.flush()
    red = HttpResponseRedirect('/')
    return red


@user_verify
def user_center_info(request):
    # 查询最近浏览商品
    browsed_obj_list = []
    if request.COOKIES.has_key('browsed'):
        browsed_list = request.COOKIES['browsed'].split('/')
        # browsed_obj_list = GoodsInfo.objects.filter(id__in=browsed_list)
        # 为了保证最近浏览商品的显示顺序和cookie里的记录一致，所以使用如下方式而没有采用如上方式
        for i in browsed_list:
            browsed_obj_list.append(GoodsInfo.objects.get(id=int(i)))

    # 查询用户信息
    user_id = request.session.get('user_id')
    user_info = Users.objects.get(id=user_id)

    context = {'active': 'info',
               'title': '个人信息',
               'user_name': user_info.uname,
               'phone': user_info.phone,
               'address': user_info.address,
               'browsed_obj_list': browsed_obj_list,
               }
    return render(request, 'users/user_center_info.html', context)


@user_verify
def user_center_order(request):
    order_info = OrderInfo.objects.filter(user_id=request.session['user_id']).order_by('-odate')
    context = {'active': 'order',
               'title': '订单',
               'order_info': order_info,
               }
    return render(request, 'users/user_center_order.html', context)


@user_verify
def user_center_site(request):
    user_id = request.session.get('user_id')
    user_info = Users.objects.get(id=user_id)

    context = {'active': 'site',
               'title': '收货地址',
               'recipient': user_info.recipient,
               'phone': user_info.phone,
               'address': user_info.address,
               }
    return render(request, 'users/user_center_site.html', context)


@user_verify
def update_address(request):
    if request.method == "POST":
        post_data = request.POST
        recipient = post_data.get('recipient')
        address = post_data.get('address')
        phone = post_data.get('phone')
        post_code = post_data.get('post_code')

        user_id = request.session.get('user_id')
        user_info = Users.objects.get(id=user_id)

        user_info.recipient = recipient
        user_info.address = address
        user_info.phone = phone
        user_info.post_code = post_code
        user_info.save()

    return redirect('/users/user_center_site')
