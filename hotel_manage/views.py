from django.shortcuts import render, redirect
from django.http import JsonResponse
from django import forms
# Create your views here.
from .models import User, Room, Guest, Order
from .do_query import *
import hashlib
from django.views.decorators.csrf import csrf_exempt


def login(request):
    """
    登陆函数，url为/login，当管理员未登陆时重定向至这里登陆完成后重定向到index
    :param request:
    :return:
    """
    session = request.session
    if 'username' in session:
        return redirect('/index')
    else:
        if request.method == "GET":
            return render(request, 'login.html')
        elif request.method == "POST":
            print(request.POST)
            try:
                username = request.POST['username']
                password = request.POST['password']
                user_query = check_user()
                print(username, password)
                if user_query.check_user(username):
                    passwd = user_query.get_password()
                    password = hashlib.md5(password.encode("utf-8")).hexdigest()
                    if passwd == password:
                        session['username'] = username
                        session['is_admin'] = 1 if user_query.get_is_admin() else 0
                        return redirect('/index')
                    else:
                        return render(request, 'login.html', {'msg': 'password error'})
                else:
                    return render(request, 'login.html', {'msg': 'username error'})
            except Exception as e:
                print(e)
                return redirect('/login')
        else:
            return redirect('/login')


def sign(request):
    """
    此函数为管理员注册函数，其url为/sign
    :param request:
    :return:
    """
    session = request.session
    if 'username' in session:
        return redirect('/index')
    else:
        if request.method == "GET":
            return render(request, 'sign.html')
        elif request.method == "POST":
            # print(request.POST)
            try:
                username = request.POST['username']
                password = request.POST['password']
                user_query = check_user()
                # print(username, password)
                if not user_query.check_user(username):
                    password = hashlib.md5(password.encode("utf-8")).hexdigest()
                    if create_user(username, password):
                        request.session['username'] = username
                        request.session['is_admin'] = 0
                        return redirect('/index')
                    else:
                        return render(request, 'sign.html', {'msg': 'create error'})
                else:
                    return render(request, 'sign.html', {'msg': 'username error'})
            except Exception as e:
                print(e)
                return redirect('/sign')
        else:
            return redirect('/sign')

@csrf_exempt
def check(request):
    """
    示例函数，开发时请加入csrf_exempt防止csrf保护
    本函数为登记函数，url为/check，当get请求时将check。html进行渲染并返回，当post时返回json。
    api 见文档
    :param request:
    :return:
    """
    session = request.session
    if 'username' not in session:
        return redirect('/login')
    elif request.method == "GET":
        return render(request, 'check_in.html')
    elif request.method == "POST":
        response_data = {}
        try:
            guest_name = request.POST['name']
            guest_id_number = request.POST['id_number']
            room_number = request.POST['room_number']
            date = request.POST['date']
            if check_room_status(room_number):
                if create_order(guest_name=guest_name, guest_c_id=guest_id_number, room_number=room_number,
                                order_date=date):
                    response_data['status'] = 'success'
                else:
                    response_data['status'] = 'error'
                    response_data['msg'] = 'create error, please call admin to get help.'
            else:
                response_data['status'] = 'error'
                response_data['msg'] = 'this room is full, please change another one.'
        except Exception as e:
            response_data['status'] = 'error'
            response_data['msg'] = 'the message is not enough, please check it.'
        finally:
            return JsonResponse(response_data)


def index(request):
    """
    index函数，渲染主页面
    :param request:
    :return:
    """
    session = request.session
    if 'username' not in session:
        return redirect('/login')
    else:
        is_admin = session['is_admin']
        return render(request, 'index.html', get_index_data(is_admin))
