# coding:utf-8
from django.shortcuts import redirect
from django.http import HttpResponseRedirect


# 在一些需要登录的模块 验证用户是否已经登录，如果已经登录，返回登录信息, 如果没有登录，则跳到登录页面(首页除外)
def user_verify(target_func):
    def wrapper(request):
        # 根据用户发来的session-id，查找服务器本地该session-id对应的session信息中有没有user_id字段
        # 有的话表示该用户已经登录
        if request.session.has_key('user_id'):
            return target_func(request)
        else:
            url = request.path
            re = HttpResponseRedirect('/login')
            re.set_cookie('url', url)
            return re
    return wrapper
