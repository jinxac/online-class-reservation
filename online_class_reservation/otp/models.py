from django.db import models
from djchoices.choices import DjangoChoices, ChoiceItem

class OtpType(DjangoChoices):
    Class = ChoiceItem(0)

# Create your models here.
class Otp(models.Model):
  otp=models.IntegerField()
  expires_at=models.DateTimeField()
  otp_type=models.IntegerField(choices=OtpType.choices, validators=[OtpType.validator])
  email=models.EmailField(max_length=254, null=True, blank=True)
  class_id=models.IntegerField(null=True, blank=True)