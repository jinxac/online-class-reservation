from exceptions.exceptions import AppException, Http400
class ExceptionCodes:
    OTP_MISSING='OTP001'
    OTP_NOT_VALID='OTP002'
    OTP_USED='OTP003'
    OTP_EXPIRED='OTP004'
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