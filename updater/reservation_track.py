from online_class.models import Class, ClassReserved, ClassReservedStatus


def reservation_track():
  queryset= ClassReserved.objects.filter(status=ClassReservedStatus.Pending)

  if queryset.exists():
    for datum in queryset:
      class_obj = datum.class_id
      class_obj.seats_booked -= 1
      if class_obj.seats_booked < 0:
        class_obj.seats_booked = 0
      class_obj.save()
      datum.status = ClassReservedStatus.Cancelled
      datum.save()
