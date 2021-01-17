from django.shortcuts import render
import json
from django.http import Http404
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination


from .models import Class, ClassStatus, User, ClassReserved, ClassConfirmed, ClassReservedStatus
from otp.models import Otp, validate_otp
from .serializer import ClassSerializer
from .exceptions import ClassUpdateException, \
  ClassSeatBookedMoreThanTotalException, \
    ReserveSeatDetailsMissingException,\
      ReserveClassConfirmedException, ReserveClassCancelledException, \
        CancelSeatDetailsMissingException, \
          ConfirmSeatCancelledException, \
            ConfirmSeatDoesNotExistException

from otp.exceptions import OtpMissingException
class ClassViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
  queryset=Class.objects.all()
  serializer_class=ClassSerializer
  def get_object(self, pk):
    try:
        return Class.objects.get(pk=pk)
    except Class.DoesNotExist:
        raise Http404

  def retrieve(self, request, pk=None):
    queryset = Class.objects.get(id=pk)
    class_object = self.get_object(pk)
    serializer = ClassSerializer(class_object)
    return Response(serializer.data)

  def create(self, request):
    serializer = ClassSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def update(self, request, pk=None):
    class_object = self.get_object(pk)
    serializer = ClassSerializer(instance=class_object, data=request.data)

    if class_object.status in [ClassStatus.Ongoing, ClassStatus.Completed]:
      # TODO: Add log
      raise ClassUpdateException()
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

  def destroy(self, request, pk=None):
    class_object = self.get_object(pk)
    if class_object.status in [ClassStatus.Ongoing, ClassStatus.Completed]:
      # TODO: Add log
      raise ClassUpdateException()
    class_object.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['POST'])
@require_http_methods(["POST"])
def reserve_class_seat(request):
  if not request.data:
    raise ReserveSeatDetailsMissingException("Please pass the data")

  class_id= request.data['class']
  user_id = request.data['user']

  if user_id is None:
    raise ReserveSeatDetailsMissingException("Please pass user id")

  if class_id is None:
    raise ReserveSeatDetailsMissingException("Please pass class id")

  try:
    class_object = Class.objects.get(id=class_id)
  except Class.DoesNotExist:
    raise ReserveSeatDetailsMissingException("Class id is incorrect")

  try:
    user = User.objects.get(id=user_id)
  except User.DoesNotExist:
    raise ReserveSeatDetailsMissingException("User id is incorrect")


  if class_object.status in [ClassStatus.Ongoing, ClassStatus.Completed]:
    raise ReserveSeatDetailsMissingException("Cannot reserve a seat in ongoing or complete class")

  if class_object.number_of_seats - class_object.seats_booked <= 0:
    raise ReserveSeatDetailsMissingException("Class is already full.. Please try next class")

  class_reserved_queryset = ClassReserved.objects.filter(
    class_id=class_object,
    user_id=user
  )

  if class_reserved_queryset.exists():
    class_confirmed_queryset = ClassConfirmed.objects.filter(
      class_id=class_object,
      user_id=user
    )

    if class_confirmed_queryset.exists():
      raise ReserveClassConfirmedException()
    else:
      otp_object = Otp.objects.get(class_id=class_id, email=user.email)
      otp_object.expires_at = timezone.now() + timedelta(minutes=5)
      otp_object.save()
  else:
    ClassReserved.objects.create(
      class_id=class_object,
      user_id=user
    )
    otp_object = Otp.objects.create(
      class_id=class_id,
      email=user.email
    )

    class_object.seats_booked += 1
    class_object.save()

  # send_mail("Confirmation OTP", "The otp for the confirmation of class is {}".format(otp_object.otp),
  #         "", ["saluja.harkirat@gmail.com"])
  return Response("Successfully reserved class with otp {}".format(otp_object.otp), status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def confirm_class_seat(request):
  if not request.data:
    raise OtpMissingException()

  otp = request.data.get("otp")

  if not otp:
    raise OtpMissingException()

  otp_object = validate_otp(otp)

  class_object = Class.objects.get(id=otp_object.class_id)
  class_reserved_object = ClassReserved.objects.get(class_id=class_object)

  if class_reserved_object.status == ClassReservedStatus.Cancelled:
    raise ReserveClassCancelledException()

  ClassConfirmed.objects.create(
    class_id=class_object,
    user_id = class_reserved_object.user_id
  )

  class_reserved_object.status=ClassReservedStatus.Confirmed
  class_reserved_object.save()
# send_mail("Class Confirmed", "Successfully confirmed class with name {}".format(class_object.name),
  #         "", ["saluja.harkirat@gmail.com"])
  return Response("Successfully confirmed class with details {}".format(class_object.id), status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def cancel_class_seat(request):
  if not request.data:
      raise ReserveSeatDetailsMissingException("Please pass the data")

  class_id= request.data['class']
  user_id = request.data['user']

  if user_id is None:
    raise CancelSeatDetailsMissingException("Please pass user id")

  if class_id is None:
    raise CancelSeatDetailsMissingException("Please pass class id")

  try:
    class_object = Class.objects.get(id=class_id)
  except Class.DoesNotExist:
    raise CancelSeatDetailsMissingException("Class id is incorrect")


  try:
    user = User.objects.get(id=user_id)
  except User.DoesNotExist:
    raise ReserveSeatDetailsMissingException("User id is incorrect")

  try:
    class_confirmed_object = ClassConfirmed.objects.get(class_id=class_object, user_id=user)
    if not class_confirmed_object.is_active:
      raise ConfirmSeatCancelledException()
  except ClassConfirmed.DoesNotExist:
    raise ConfirmSeatDoesNotExistException()

  class_object.seats_booked -= 1
  class_object.save()

  class_confirmed_object.is_active = False
  class_confirmed_object.save()

  return Response("Successfully cancelled class", status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
def get_report(request):
  class_queryset = Class.objects.all()
  number_of_classes = class_queryset.count()
  number_of_users = User.objects.count()

  number_of_active_classes =class_queryset.filter(status=ClassStatus.Ongoing).count()
  number_of_upcoming_classes = class_queryset.filter(status=ClassStatus.Upcoming).count()
  number_of_completed_classes = class_queryset.filter(status=ClassStatus.Completed).count()

  confirmed_seats = []

  for datum in class_queryset:
    confirmed_seats.append({
      "class_id": datum.id,
      "seats_booked": datum.seats_booked
    })

  data = {
    "number_of_classes": number_of_classes,
    "number_of_users": number_of_users,
    "confirmed_seats": confirmed_seats,
    "number_of_active_classes": number_of_active_classes,
    "number_of_upcoming_classes": number_of_upcoming_classes,
    "number_of_completed_classes": number_of_completed_classes
  }

  return Response(data, status=status.HTTP_200_OK)
