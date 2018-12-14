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


class check_user():
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
    try:
        User(user_username=username, user_password=password, is_admin=False).save()
        return True
    except Exception as e:
        print(e)
        return False
    
def get_index_data(is_admin):
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
        'y_money':total_money,
        'm_money':total_money,
        'is_admin':is_admin,
        'bills': [{
            'date': today_date,
            'money': total_money,
            'room': total_live_room,
            'live_percent': live_percent
        }]
    }
    return recv_data
    
    