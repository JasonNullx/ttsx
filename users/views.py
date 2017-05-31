from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def register(request):
    return render(request, 'users/register.html')


def register_action(request):
    post_data = request.POST
    username = post_data.get('username')
    password = post_data.get('pwd')
    cpwd = post_data.get('cpwd')
    email = post_data.get('email')

    return HttpResponse(str)


def login(request):
    pass


def user_center(request):
    pass
