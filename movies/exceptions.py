from rest_framework.exceptions import APIException

class ReviewException(APIException):
    status_code = 422
    default_detail = 'You already made this review.'