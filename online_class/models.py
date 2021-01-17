from django.db import models
from django.db.models import UniqueConstraint
from djchoices.choices import ChoiceItem, DjangoChoices
from django.core.validators import MinLengthValidator

from .exceptions import ClassSeatBookedMoreThanTotalException

# Create your models here.
class ClassType(models.Model):
  name=models.CharField(max_length=100)
  code=models.CharField(max_length=100, unique=True)


class ClassStatus(DjangoChoices):
    Upcoming = ChoiceItem(0)
    Ongoing  = ChoiceItem(1)
    Completed = ChoiceItem(2)

class Class(models.Model):
  name=models.CharField(max_length=100)
  class_type=models.ForeignKey(ClassType, related_name="class_type", on_delete=models.CASCADE)
  total_sessions=models.PositiveIntegerField()
  number_of_seats=models.PositiveIntegerField()
  seats_booked=models.PositiveIntegerField()
  status=models.IntegerField(choices=ClassStatus.choices, validators=[ClassStatus.validator], default=ClassStatus.Upcoming)
  start_date=models.DateTimeField(auto_now_add=True,null=True, blank=True)
  end_date=models.DateTimeField(null=True, blank=True)
  is_active=models.BooleanField(default=True)

  def save(self, *args, **kwargs):
    if self.seats_booked > self.number_of_seats:
      raise ClassSeatBookedMoreThanTotalException()

    super().save(*args, **kwargs)

class User(models.Model):
  name=models.CharField(max_length=200)
  phone_number = models.CharField(max_length=15,validators=[MinLengthValidator(8)])
  email = models.EmailField(max_length=254)


class ClassReservedStatus(DjangoChoices):
  Pending=ChoiceItem(0)
  Confirmed=ChoiceItem(1)
  Cancelled=ChoiceItem(2)

class ClassReserved(models.Model):
  class_id=models.ForeignKey(Class, related_name="class_reserved_class_id", on_delete=models.CASCADE)
  status=models.IntegerField(choices=ClassReservedStatus.choices, validators=[ClassReservedStatus.validator], default=ClassReservedStatus.Pending)
  user_id=models.ForeignKey(User, related_name="class_reserved_user_id", on_delete=models.CASCADE)

class ClassConfirmed(models.Model):
  class_id=models.ForeignKey(Class, related_name="class_confirmed_class_id", on_delete=models.CASCADE)
  is_active=models.BooleanField(default=True)
  user_id=models.ForeignKey(User, related_name="class_confirmed_user_id", on_delete=models.CASCADE)

