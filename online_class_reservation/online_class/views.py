from django.shortcuts import render
import json
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Class, ClassStatus, User, ClassReserved
from otp.models import Otp
from .serializer import ClassSerializer
from .exceptions import ClassUpdateException, ReserveSeatDetailsMissing


class ClassViewSet(viewsets.ViewSet):
  def list(self, request):
    queryset=Class.objects.all()
    start_date = self.request.query_params.get('start_date', None)
    class_type = self.request.query_params.get('class_type', None)
    status = self.request.query_params.get('status', None)


    # Add page number and page size filter to this
    # add booking status filter

    if start_date:
      queryset = queryset.filter(class__start_date=start_date)

    if class_type:
      queryset = queryset.filter(class__class_type=class_type)

    if status:
      queryset = queryset.filter(class__status= status)

    serializer=ClassSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk=None):
    queryset = Class.objects.all()
    class_object = get_object_or_404(queryset, pk=pk)
    serializer = ClassSerializer(class_object)
    return Response(serializer.data)

  def create(self, request):
    serializer = ClassSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)

  def update(self, request, pk=None):
    class_object = Class.objects.get(id=pk)
    serializer = ClassSerializer(instance=class_object, data=request.data)

    if class_object.status in [ClassStatus.Ongoing, ClassStatus.Completed]:
      # TODO: Add log
      raise ClassUpdateException()
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

  def destroy(self, request, pk=None):
    class_object = Class.objects.get(id=pk)
    if class_object.status in [ClassStatus.Ongoing, ClassStatus.Completed]:
      # TODO: Add log
      raise ClassUpdateException()
    class_object.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@require_http_methods(["POST"])
def reserve_class_seat(self, request):
  load_data = json.load(request.data)
  class_id= load_data.data['class']
  user_id = load_data.data['user']

  if user_id is None:
    raise ReserveSeatDetailsMissing("Please pass user id")

  if class_id is None:
    raise ReserveSeatDetailsMissing("Please pass class id")

  try:
    class_object = Class.objects.get(id=class_id)
  except Class.DoesNotExist:
    raise ReserveSeatDetailsMissing("Class id is incorrect")

  try:
    user = User.object.get(id=user_id)
  except User.DoesNotExist:
    raise ReserveSeatDetailsMissing("User id is incorrect")


  if class_object.status in [ClassStatus.Ongoing, ClassStatus.Completed]:
    raise ReserveSeatDetailsMissing("Cannot reserve a seat in ongoing or complete class")

  if not class_object.total_seats - class_object.seats_booked:
    raise ReserveSeatDetailsMissing("Class is already full.. Please try next class")

  ClassReserved.objects.create(class_id=class_object)
  otp_object = Otp.objects.create(
    class_id=class_id,
    email=user.email
  )

  # Todo: send email
  return Response("Successfully reserved class with otp {}".format(otp_object.otp), status=status.HTTP_200_OK)

