from django.shortcuts import render, redirect
from django.http import JsonResponse
from django import forms

# Create your views here.

from .models import User, Room, Guest, Order
from .do_query import *
import hashlib
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
import json


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
        recv_data = json.loads(request.body)
        try:
            guest_name = recv_data['name']
            guest_id_number = recv_data['id_number']
            room_number = recv_data['room_number']
            date = recv_data['date']
            if check_room_status(room_number, guest_id_number):
                if create_order(guest_name=guest_name, guest_c_id=guest_id_number, room_number=room_number,
                                order_date=date):
                    response_data['status'] = 'success'
                else:
                    response_data['status'] = 'error'
                    response_data['msg'] = 'create error, please call admin to get help.'
            else:
                response_data['status'] = 'error'
                response_data['msg'] = 'this room is full or you have check in here, please change another one.'
        except Exception as e:
            print(e)
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



@csrf_exempt
def settle(request):
    '''
    [查询]按钮功能
    返回结账订单
    requests
    {
        'name':'',
        'id_number':'xxxx'
    }
    response
    {
        'id_number':'',
        'name':'',
        'order':[
        {
            'id':'',
            'room_number':'',
            'date':'',
            'price':''
        },
        ]
    }
    :param request:
    :return:
    '''
    session = request.session
    if 'username' not in session:
        return redirect('/index')
    else:
        if request.method == "GET":
            return render(request, 'settle.html')
        elif request.method == "POST":
            response_data = {}
            request_data = json.loads(request.body)
            try:
                #######  客户名与身份证号 前端提交的数据
                guest_name = request_data['name']
                guest_id_number = request_data['id_number']
                #######
                guest = Guest.objects.filter(guest_c_id = guest_id_number).first()
                orders = Order.objects.filter(guest = guest)
                response_data['id_number'] = guest_id_number
                response_data['name'] = guest_name
                response_data['orders'] = []
                response_data['status'] = 'success'
                for order in orders:
                    info = {}
                    info['id_number'] = guest_id_number
                    info['name'] = guest_name
                    info['id'] = order.id
                    info['room_number'] = order.room.room_number
                    info['date'] = str(order.order_date)
                    info['price'] = order.room.room_price
                    response_data['orders'].append(info)
                return JsonResponse(response_data)
            except:
                return None


@csrf_exempt
def settle_finish(request):
    '''
    [结账]按钮功能    一个客户有多个订单就多次调用此函数
    requests
    {
        'order_id':'xx',
    }
    response
    {
        'status':'xxx',
        'msg':'xxxx'
    }
    :param request:
    :return:
    '''
    session = request.session
    if 'username' not in session:
        return redirect('/index')
    else:
        response_data = {}
        request_data = json.loads(request.body)
        try:
            orders = [Order.objects.get(id=order_id) for order_id in request_data['order_id']]
        except:
            response_data['status'] = 'error'
            response_data['msg'] = "order doesn't exist"
            return JsonResponse(response_data)
        try:
            #修改房间状态为空
            for order in orders:
                order.room.status = '0'
                order.room.save()
                order.is_finish = True
                order.save()
            response_data['status'] = 'success'
            response_data['msg'] = "order is finished"
            return JsonResponse(response_data)
        except:
            response_data['status'] = 'error'
            response_data['msg'] = "failed"
            return JsonResponse(response_data)


@csrf_exempt
def group_book(request):
    '''
    团体预定
    requests
    {
        'org_name':'xx',
        'member':[{
            'name':'',
            'id_number':'',
            'room_number':''
        }
        ...],
        'date':''
    }
    response
    {
        'status':['seccuss'.'error'],
        'msg':'xxx'
    }
    '''
    session = request.session
    if 'username' not in session:
        return redirect('/index')
    else:
        if request.method == "GET":
            return render(request, 'group_book.html')
        elif request.method == "POST":
            response_data = {}
            try:
                ####### 前端提交的数据
                org_name = request.POST['org_name']
                member = request.POST['member']
                order_date = request.POST['date']
                #######
                for i in member:
                    guest = add_guest(i['name'],i['id_number'])
                    guest.update(is_group = True,group_name = org_name)
                    if not check_room_status(i['room_number']):
                        response_data['status'] = 'error'
                        response_data['msg'] = 'A room has been lived'
                        return JsonResponse(response_data)
                    else:
                        if create_order(i['name'],i['id_number'],i['room_number'],order_date):
                            continue
                        else:
                            response_data['status'] = 'error'
                            response_data['msg'] = 'Create orders failed'
                            return JsonResponse(response_data)
                response_data['status'] = 'success'
                response_data['msg'] = "Group book succssed"
                return JsonResponse(response_data)
            except:
                response_data['status'] = 'error'
                response_data['msg'] = "Group book faied"
                return JsonResponse(response_data)


@csrf_exempt
def group_settle(request):
    '''
    requests
    {
        'org_name':'xx',
    }
    response
    {
        'orders':[{
            'id':'xx',
            'id_number':'xxx',
            'name':'xxx',
            'room_number':'xx',
            'date':'xxx',
            'price':'xxx',
    }
    :param request:
    :return:
    '''
    session = request.session
    if 'username' not in session:
        return redirect('/index')
    else:
        if request.method == "GET":
            return render(request, 'settle.html')
        elif request.method == "POST":
            response_data = {}
            response_data['order'] = []
            try:
                org_name = request.POST['org_name']
                #团体里所有顾客的集合
                guests = Guest.objects.filter(group_name = org_name)
                for guest in guests:
                    orders = Order.objects.fliter(guest = guest)
                    for order in orders:
                        info = {}
                        info['id'] = order.id
                        info['id_number'] = guest.guest_c_id
                        info['name'] = guest.guest_name
                        info['room_number'] = order.room.room_number
                        info['data'] = str(order.order_date)
                        info['price'] = order.room.room_price
                        response_data['order'].append(info)
                return JsonResponse(response_data)
            except:
                return None

@csrf_exempt
def group_settle_finish(request):
    '''
    requests
    {
        'order_ids':[id1,id2,……],
    }
    response
    {
        'status':'xxx',
        'msg':'xxxx'
    }
    :param request:
    :return:
    '''
    session = request.session
    if 'username' not in session:
        return redirect('/index')
    else:
        response_data = {}
        try:
            ####### 订单编号 前端提交的数据
            order_ids = request.POST['order_id']
            #######
            order_list = []
            for i in order_ids:
                order = Order.objects.filter(id=i).first()
                order_list.append(order_list)
        except:
            response_data['status'] = 'error'
            response_data['msg'] = "order doesn't exist"
            return JsonResponse(response_data)
        try:
            for order in order_list:
                # 修改房间状态为空
                order.room.status = '0'
                order.room.save()
                # 修改客户状态 退出团体
                order.guest.is_group = False
                order.guest.group_name = ''
                order.guest.save()
                order.is_finish = True
                order.save()
            response_data['status'] = 'success'
            response_data['msg'] = "order is finished"
            return JsonResponse(response_data)
        except:
            response_data['status'] = 'error'
            response_data['msg'] = "failed"
            return JsonResponse(response_data)


def check_guest_info(request):
    session = request.session
    pass


def check_room(request):
    '''
    :param request:
    :return: {"cost": res_money}
    '''
    session = request.session
    if 'uesrname' not in session:
        return redirect('/login')
    else:
        if request.method == "GET":
            return render(request, 'index.html')
        elif request.method == "POST":
            try:
                room_id = request.POST['room_id']
                days = Order.objects.filter(room_id).count()
                price = Room.objects.get(room_number=room_id).room_price
                res_money = days * price

                return render(request, 'check_room.html', {"cost": res_money})
            except:
                pass

    pass


# 结账报表:  用户名  入住时间  退房时间  入住天数  入住房间号  入住房间类型 房间单价 入住花费
# lnylgk
'''
def check_report(request):
    session = request.session
    if 'username' not in session:
        return redirect('/login')
    else:
        username = request.POST['username']
        room_id = Order.objects.get()
        in_time =
        out_time =
        days =
        room_type =
        price =
        cost =
        # 将所有信息返回之后，在数据库中删除该订单的所有信息
        DelRoomRecord =
        return render(request, '', {'username': username,
                                    'room_id': room_id,
                                    'in_time': in_time,
                                    'out_time': out_time,
                                    'days': days,
                                    'room_type': room_type,
                                    'price': price,
                                    'cost': cost})
'''


def change_room(request):
    '''
    :param request:
    :return: none
    '''
    sessio = request.session
    if 'username' not in sessio:
        return redirect('/login')
    else:
        username = request.POST['username']
        if User.objects.filter(user_username=username).is_admin:
            # 更改房价 根据房间类型
            room_type = request.POST['room_type']
            change_to_price = request.POST['change_to_price']
            ChangeRoomPrice = Room.objects.filter(room_type=room_type).update(room_price=change_to_price)
            # 更改房间类型
            room_id = request.POST['room_id']
            change_to_type = request.POST['change_to_type']
            ChangeRoomType = Room.objects.filter(room_number=room_id).update(room_type=change_to_type)
            # 增删客房
            add_room_id = request.POST['add_room_id']
            del_room_id = request.POST['del_room_id']
            AddRoom = Room.objects.create(room_nuber=add_room_id)
            DelRoom = Room.objects.filter(room_number=del_room_id).delete()

        else:
            return render(request, 'index.html', {'msg': 'you are not admin!'})