from rest_framework.exceptions import APIException
from rest_framework import status


class Http400(Exception):
    http_code = 400

class ExceptionCodes:
    CLASS_UPDATE = 'CLS001'
    CLASS_SEATS_BOOKED_MORE_THAN_TOTAL='CLS002'
    RESERVE_SEAT_DETAILS='RS001'
    RESERVE_CLASS_CONFIRMED='RS002'

class AppException(APIException):
  status_code = status.HTTP_400_BAD_REQUEST

  def __init__(self, message, error_code, params=None):
    self.message=message
    self.error_code=error_code
    self.detail={
      "message": self.message,
      "error_code": self.error_code
    }

class ClassUpdateException(AppException, Http400):
    def __init__(self, message='Cannot update ongoing or completed class', params=None):
        super(ClassUpdateException, self).__init__(message, ExceptionCodes.CLASS_UPDATE, params=params)

class ClassSeatBookedMoreThanTotalException(AppException, Http400):
    def __init__(self, message='Class seats booked cannot be more than total', params=None):
      super(ClassSeatBookedMoreThanTotalException, self).__init__(message, ExceptionCodes.CLASS_SEATS_BOOKED_MORE_THAN_TOTAL, params=params)

class ReserveSeatDetailsMissingException(AppException, Http400):
    def __init__(self, message='Please pass details...', params=None):
      super(ReserveSeatDetailsMissingException, self).__init__(message, ExceptionCodes.RESERVE_SEAT_DETAILS, params=params)

class ReserveClassConfirmedException(AppException, Http400):
    def __init__(self, message='Reserved class has already been confirmed', params=None):
      super(ReserveClassConfirmedException, self).__init__(message, ExceptionCodes.RESERVE_CLASS_CONFIRMED, params=params)