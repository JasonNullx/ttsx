# coding:utf-8


# 验证用户是否已经登录，如果已经登录，返回登录信息
def user_verify():
    user_id = request.session.get('user_id', None)
    if user_id is None:
        context['logined'] = False
        return render(request, 'index.html', context)
    else:
        uname = Users.objects.get(id=int(user_id)).uname
        context['logined'] = True
        context['uname'] = uname
        return render(request, 'index.html', context)