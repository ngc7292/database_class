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
                guest = Guest.objects.filter(guest_c_id=guest_id_number).first()
                orders = Order.objects.filter(guest=guest, is_finish=False)
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
            orders = [Order.objects.get(id=order_id, is_finish=False) for order_id in request_data['order_id']]
        except:
            response_data['status'] = 'error'
            response_data['msg'] = "order doesn't exist"
            return JsonResponse(response_data)
        try:
            # 修改房间状态为空
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
            request_data = json.loads(request.body)
            
            ####### 前端提交的数据
            org_name = request_data['org_name']
            member = request_data['members']
            order_date = request_data['date']
            #######
            for i in member:
                guest = add_guest(i['name'], i['id_number'])
                guest.is_group = True
                guest.group_name = org_name
                guest.save()
                if not check_room_status(i['room_number'], i['id_number']):
                    response_data['status'] = 'error'
                    response_data['msg'] = 'A room has been lived'
                    return JsonResponse(response_data)
                else:
                    if create_order(i['name'], i['id_number'], i['room_number'], order_date):
                        continue
                    else:
                        response_data['status'] = 'error'
                        response_data['msg'] = 'Create orders failed'
                        return JsonResponse(response_data)
            response_data['status'] = 'success'
            response_data['msg'] = "Group book succssed"
            return JsonResponse(response_data)
            # except:
            #     response_data['status'] = 'error'
            #     response_data['msg'] = "Group book faied"
            #     return JsonResponse(response_data)


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
            return render(request, 'group_settle.html')
        elif request.method == "POST":
            response_data = {}
            response_data['orders'] = []
            request_data = json.loads(request.body)
            org_name = request_data['org_name']
            # 团体里所有顾客的集合
            guests = Guest.objects.filter(group_name=org_name)
            for guest in guests:
                orders = Order.objects.filter(guest=guest, is_finish=False)
                response_data['status'] = 'success'
                for order in orders:
                    info = {}
                    info['id'] = order.id
                    info['id_number'] = guest.guest_c_id
                    info['name'] = guest.guest_name
                    info['room_number'] = order.room.room_number
                    info['date'] = str(order.order_date)
                    info['price'] = order.room.room_price
                    response_data['orders'].append(info)
            return JsonResponse(response_data)


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


@csrf_exempt
def get_guest_info(request):
    session = request.session
    if 'username' not in session:
        return redirect('')
    elif request.method == "GET":
        return render(request, 'check_guest_info.html')
    elif request.method == "POST":
        request_data = json.loads(request.body)
        guest_name = request_data['name']
        guest_c_id = request_data['id_number']
        guest = Guest.objects.get(guest_c_id=guest_c_id)
        orders = Order.objects.filter(guest=guest)
        response_data = {}
        response_data['status'] = 'success'
        response_data['orders'] = []
        for order in orders:
            response_data['orders'].append({
                'id': order.id,
                'id_number': guest.guest_c_id,
                'name': guest.guest_name,
                'date': order.order_date,
                'room_number': order.room.room_number,
                'price': order.room.room_price
            })
        return JsonResponse(response_data)


@csrf_exempt
def check_room(request):
    '''
    :param request:
    :return: {"room": [{
        'id':,
        'number':,
        'type':,
        'price':,
        'status':
        }]}
    '''
    session = request.session
    if 'username' not in session:
        return redirect('/login')
    else:
        if request.method == "GET":
            response_data = {}
            response_data['rooms'] = []
            try:
                # 查询所有的房间
                rooms = Room.objects.all()
                for room in rooms:
                    response_data['rooms'].append(
                        {
                            'id': room.id,
                            'room_number': room.room_number,
                            'room_type': room.room_type.room_type,
                            'room_price': room.room_price,
                            'room_status': room.status
                        }
                    )
            except Exception as e:
                print(e)
                response_data['rooms'].append({
                    'room_id': 'None',
                    'room_number': 'None',
                    'room_type': 'None',
                    'room_price': 'None',
                    'room_status': 'None'
                })
            finally:
                return render(request, 'check_room.html', response_data)


@csrf_exempt
def change_room(request):
    '''
    request{
        'method':'change_price'/'change_type'/'add_room'/'del_room',
        'param':{
            'room_number':'',
            'room_type':'',
            'room_price':''
        }
        }
    response{
        'status':'success'/'error',
        'msg':
        }
    :param request:
    :return: none
    '''
    session = request.session
    if 'username' not in session:
        return redirect('/login')
    else:
        if request.method == "GET":
            response_data={'rooms':[]}
            rooms = Room.objects.all()
            for room in rooms:
                response_data['rooms'].append(
                    {
                        'id': room.id,
                        'room_number': room.room_number,
                        'room_type': room.room_type.room_type,
                        'room_price': room.room_price,
                        'room_status': room.status
                    }
                )
            return render(request, 'change_room.html',response_data)
        elif request.method == "POST":
            response_data = {}
            request_data = json.loads(request.body)
            if request_data['method'] == 'change_price':
                try:
                    room = Room.objects.filter(room_number=
                                               request_data['param']['room_number']).update(
                        room_price=request_data['param']['room_price'])
                except:
                    response_data['status'] = 'error'
                    response_data['msg'] = 'Change Price failed'
                    return JsonResponse(response_data)
                response_data['status'] = 'success'
                response_data['msg'] = 'Change Price success'
            elif request_data['method'] == 'change_type':
                try:
                    room_type = Room_type.objects.filter(room_type=request_data['param']['room_type']).first()
                    room = Room.objects.filter(room_number=
                                               request_data['param']['room_number']).update(room_type=room_type)
                except:
                    response_data['status'] = 'error'
                    response_data['msg'] = 'Change Type failed'
                    return JsonResponse(response_data)
                response_data['status'] = 'success'
                response_data['msg'] = 'Change Type success'
            elif request_data['method'] == 'add_room':
                try:
                    room_type = Room_type.objects.filter(room_type=request_data['param']['room_type']).first()
                    room = Room.objects.create(room_type=room_type, room_number=request_data['param']['room_number']
                                               , room_price=request_data['param']['room_price'], status='0')
                except:
                    response_data['status'] = 'error'
                    response_data['msg'] = 'Add Room failed'
                    return JsonResponse(response_data)
                response_data['status'] = 'success'
                response_data['msg'] = 'Add Room success'
            elif request_data['method'] == 'del_room':
                try:
                    room = Room.objects.filter(room_number=request_data['param']['room_number']).delete()
                except:
                    response_data['status'] = 'error'
                    response_data['msg'] = 'Delete Room failed'
                    return JsonResponse(response_data)
                response_data['status'] = 'success'
                response_data['msg'] = 'Delete Room success'
            return JsonResponse(response_data)