from rest_framework.exceptions import APIException
from rest_framework import status

class Http400(Exception):
    http_code = 400

class AppException(APIException):
  status_code = status.HTTP_400_BAD_REQUEST

  def __init__(self, message, error_code, params=None):
    self.message=message
    self.error_code=error_code
    self.detail={
      "message": self.message,
      "error_code": self.error_code
    }