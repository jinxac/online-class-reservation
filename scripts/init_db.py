import django
import os
import datetime
import random


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "online_class_reservation.settings")
django.setup()

from online_class.models import Class, ClassType, User

class_type_mock = [
  {
    "name": "first type",
    "code": "A001"
  },
  {
    "name": "second type",
    "code": "A002"
  }
]

class_mock = [
  {
    "name": "first class",
    "total_sessions": 100,
    "number_of_seats": 50,
    "seats_booked": 45
  },
    {
    "name": "second class",
    "total_sessions": 100,
    "number_of_seats": 50,
    "seats_booked": 10
  }
]

user_mock = [
  {
    "name": "Harkirat",
    "phone_number": "9886268129",
    "email": "saluja.harkirat@gmail.com"
  },
    {
    "name": "Rahul",
    "phone_number": "9886268132",
    "email": "test@abc.com"
  }
]

for datum in class_type_mock:
  ClassType.objects.create(name=datum['name'], code=datum['code'])

for datum in class_mock:
  Class.objects.create(name=datum['name'],
    class_type=ClassType.objects.order_by('?').first(),
    total_sessions=datum['total_sessions'],
    number_of_seats=datum['number_of_seats'],
    seats_booked=datum['seats_booked']
    )

for datum in user_mock:
  User.objects.create(name=datum['name'], phone_number=datum['phone_number'], email=datum['email'])