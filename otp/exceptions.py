from rest_framework.exceptions import APIException
from rest_framework import status


class Http400(Exception):
    http_code = 400

class ExceptionCodes:
    OTP_MISSING='OTP001'
    OTP_NOT_VALID='OTP002'
    OTP_USED='OTP003'
    OTP_EXPIRED='OTP004'

class AppException(APIException):
  status_code = status.HTTP_400_BAD_REQUEST

  def __init__(self, message, error_code, params=None):
    self.message=message
    self.error_code=error_code
    self.detail={
      "message": self.message,
      "error_code": self.error_code
    }

class OtpMissingException(AppException, Http400):
  def __init__(self, message='Please pass the otp', params=None):
      super(OtpMissingException, self).__init__(message, ExceptionCodes.OTP_MISSING, params=params)

class OtpNotValidException(AppException, Http400):
  def __init__(self, message='Please pass the correct otp', params=None):
      super(OtpNotValidException, self).__init__(message, ExceptionCodes.OTP_NOT_VALID, params=params)

class OtpUsedException(AppException, Http400):
  def __init__(self, message='Otp has already been used', params=None):
      super(OtpUsedException, self).__init__(message, ExceptionCodes.OTP_USED, params=params)

class OtpExpiredException(AppException, Http400):
  def __init__(self, message='Otp has already been used', params=None):
      super(OtpExpiredException, self).__init__(message, ExceptionCodes.OTP_EXPIRED, params=params)