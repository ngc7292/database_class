#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path
from django.conf.urls import url
from .views import login

urlpatterns = [
    url('login/', login)
]