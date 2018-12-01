from django.test import TestCase

# Create your tests here.

from hotel_manage.models import Room, Guest


class TestDB(TestCase):
    def setUp(self):
        Room(room_number="101", room_type="SR", room_price=300).save()
        Room(room_number="102", room_type="SR", room_price=300).save()
        Room(room_number="103", room_type="TR", room_price=400).save()
        Room(room_number="104", room_type="FR", room_price=500).save()
    
    def test_guest_live_room(self):
        room = Room.objects.get(room_number="101")
        g = Guest(guest_name="李瑞", guest_c_id="371102199901277810", guest_status="OR", group_name="")
        g.save()
        