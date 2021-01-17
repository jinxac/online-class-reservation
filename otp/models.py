from django.db import models
from django.utils import timezone
from djchoices.choices import DjangoChoices, ChoiceItem
import random
from datetime import timedelta

from .exceptions import OtpMissingException, OtpNotValidException, OtpUsedException, OtpExpiredException

class OtpType(DjangoChoices):
    Class = ChoiceItem(0)

def generate_otp():
    return random.randint(10000, 99999)

# Create your models here.
class Otp(models.Model):
  otp=models.IntegerField()
  expires_at=models.DateTimeField()
  otp_type=models.IntegerField(choices=OtpType.choices, validators=[OtpType.validator], default=OtpType.Class)
  email=models.EmailField(max_length=254, null=True, blank=True)
  used_at = models.DateTimeField(null=True, blank=True)
  class_id=models.IntegerField(null=True, blank=True)

  def save(self, force_insert=False,force_update=False, using=None,
        update_fields=None):
    if self.pk is None:
      self.otp = generate_otp()
      self.expires_at = timezone.now() + timedelta(minutes=5)

    return super(Otp, self).save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


def validate_otp(otp, email=None):
  if not otp:
    raise OtpMissingException()

  queryset = Otp.objects.filter(otp=otp)

  if email:
    queryset = queryset.filter(email)


  if not queryset.exists():
    raise OtpNotValidException()

  queryset = queryset.filter(used_at__isnull=True)

  if not queryset.exists():
    raise OtpUsedException()

  otp_object = queryset[0]

  if otp_object.expires_at < timezone.now():
    raise OtpExpiredException()


  otp_object.used_at = timezone.now()
  otp_object.save()

  return otp_object


