#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'ralph'
__mtime__ = '2018/12/4'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
             ┏┓   ┏┓
            ┏┛┻━━━┛┻┓
            ┃       ┃
            ┃ ┳┛ ┗┳ ┃
            ┃   ┻   ┃
            ┗━┓   ┏━┛
              ┃   ┗━━━┓
              ┃神兽保佑┣┓
              ┃永无BUG  ┏┛
              ┗┓┓┏━┳┓┏━┛
               ┃┫┫ ┃┫┫
               ┗┻┛ ┗┻┛
"""
from .models import *
from datetime import date
import django


"""
数据库交互脚本，所有关于数据库的操作封装在这里
"""

class check_user:
    """
    检查用户的类，用于查看用户是否存在，获取其密码，以及获取其是否为管理员，
    初始化类后必须调用check_user，若返回true才可以进行下一步操作
    """
    def __init__(self):
        self.user_query = None
    
    def check_user(self, username):
        try:
            self.user_query = User.objects.get(user_username=username)
            return True
        except Exception as e:
            return False
    
    def get_password(self):
        return self.user_query.user_password
    
    def get_is_admin(self):
        return self.user_query.is_admin


def create_user(username, password):
    """
    创建用户
    :param username:
    :param password:
    :return:
    """
    try:
        User(user_username=username, user_password=password, is_admin=False).save()
        return True
    except Exception as e:
        print(e)
        return False


def get_index_data(is_admin):
    """
    获取主页面的数据
    :param is_admin: 是否为主管理员，用于渲染控制部分
    :return:
    """
    orders = []
    total_money = 0
    total_live_room = 0
    total_room = Room.objects.all().count()
    today_date = date.today().isoformat()
    
    room_numbers = []
    orders_data = Order.objects.filter(order_date=today_date)
    for order in orders_data:
        order_data = {
            'name': Guest.objects.get(id=order.guest_id).guest_name,
            'room_number': Room.objects.get(id=order.room_id).room_number
        }
        orders.append(order_data)
        if order_data['room_number'] in room_numbers:
            continue
        else:
            room_numbers.append(order_data['room_number'])
        total_live_room += 1
        total_money += Room.objects.get(id=order.room_id).room_price
    try:
        valid_room = total_room - total_live_room
        live_percent = str(total_live_room/total_room*100).split(".")[0]+"%"
    except:
        valid_room = "0"
        live_percent = "0%"
    recv_data = {
        't_live': total_live_room,
        'live_percent': live_percent,
        'valid': str(valid_room),
        'orders': orders,
        'y_money': total_money,
        'm_money': total_money,
        'is_admin': is_admin,
        'bills': [{
            'date': today_date,
            'money': total_money,
            'room': total_live_room,
            'live_percent': live_percent
        }]
    }
    return recv_data


def check_room_status(room_number, id_number):
    """
    获取房间状态（今日是否有人住在这个房间中）
    :param room_number: 房间编号
    :return:
    """
    try:
        room = Room.objects.get(room_number=room_number)
        not_f_order = Order.objects.filter(room=room, is_finish=False)
        live_number = 0
        live_guest = []
        for order in not_f_order:
            if order.guest not in live_guest:
                live_guest.append(order.guest)
                live_number += 1
            else:
                continue
        for guest in live_guest:
            if guest.guest_c_id == id_number:
                return False
        room_capcity = room.room_type.capacity
        if room_capcity > live_number:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def add_guest(guest_name, guest_c_id):
    """
    增加顾客，若存在顾客，直接返回guest类，若不存在，创建后返回
    :param guest_name:
    :param guest_c_id:
    :return:
    """
    try:
        guest = Guest(guest_name=guest_name, guest_c_id=guest_c_id)
        guest.save()
        return guest
    except django.db.utils.IntegrityError:
        guest = Guest.objects.get(guest_name=guest_name, guest_c_id=guest_c_id)
        return guest
    except Exception as e:
        print(e)
        return False


def create_order(guest_name, guest_c_id, room_number, order_date):
    """
    创建订单
    :param guest_name:
    :param guest_c_id:
    :param room_number:
    :param order_date:
    :return:
    """
    try:
        guest = add_guest(guest_name, guest_c_id)
        if not check_room_status(room_number,guest_c_id):
            return False
        else:
            room = Room.objects.get(room_number=room_number)
        today_date = date.today()
        year, month, day = order_date.split("-")
        order_date = date(int(year), int(month), int(day))
        if order_date < today_date:
            return False
        elif order_date > today_date:
            Order(guest=guest, room=room, is_reverse=True, reverse_date=order_date.isoformat()).save()
        else:
            Order(guest=guest, room=room).save()
        return True
    except Exception as e:
        print(e)
        return False
