#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    url('login/', login),
    url('index/', index),
    url('sign/', sign),
    url('change_room/', change_room),
    url('check_room/', check_room),
    url('check/', check),
    url('get_guest/', get_guest_info),
    url('group_settle/', group_settle),
    url('settle/', settle),
    url('settle_finish/', settle_finish),
    url('group/', group_book),
    url('group_settle_finish/', group_settle_finish),
]