from datetime import date

from django.db import models


# Create your models here.

class Room_type(models.Model):
    room_type = models.CharField(max_length=128)
    
    capacity = models.IntegerField()


class Room(models.Model):
    status_list = (
        ('1', 'have been reserved'),
        ('2', 'have been lived in'),
        ('0', 'empty')
    )
    
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey('Room_type', on_delete=models.CASCADE)
    
    room_price = models.IntegerField()
    status = models.CharField(max_length=2, choices=status_list, default="NO")


class Guest(models.Model):
    guest_name = models.CharField(max_length=10)
    guest_c_id = models.CharField(max_length=18, unique=True)
    
    is_group = models.BooleanField(default=False)
    group_name = models.CharField(max_length=128, blank=True)


class Order(models.Model):
    order_date = models.DateField(default=date.today)
    
    room = models.ForeignKey('Room', on_delete=models.CASCADE, to_field='room_number')
    guest = models.ForeignKey('Guest', on_delete=models.CASCADE, to_field='guest_c_id')
    
    is_reverse = models.BooleanField(default=False)
    reverse_date = models.DateField(blank=True, default=date.today)
    
    is_finish = models.BooleanField(default=False)


class User(models.Model):
    user_username = models.CharField(max_length=1024)
    user_password = models.CharField(max_length=64)
    
    is_admin = models.BooleanField(default=False)
