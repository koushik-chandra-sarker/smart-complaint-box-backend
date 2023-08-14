from django.db import OperationalError
from django.http import Http404
from rest_framework.views import APIView, exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError
from rest_framework import status


class GlobalException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST  # Set the desired HTTP status code
    message = 'Custom error message'  # Set the default error message


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    response_data = {
        'message': 'An error occurred.',
    }
    if isinstance(exc, Http404):
        response_data["message"] = "Not found."
        response_data["status_code"] = 404
    elif isinstance(exc, GlobalException):
        response_data["message"] = exc.message
        response_data["status_code"] = exc.status_code
    elif isinstance(exc, APIException):
        response_data["message"] = exc.detail
        response_data["status_code"] = exc.status_code
    elif isinstance(exc, ValidationError):
        response_data["message"] = exc.detail
        response_data["status_code"] = 400  # Bad Request for validation errors
    elif isinstance(exc, OperationalError):
        response_data["message"] = str(exc)
        response_data["status_code"] = 500  # Bad Request for validation errors
        return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if response is None:
            response_data["message"] = str(exc)
            response = Response(response_data)
            return response
        else:
            response_data["message"] = str(exc)
            response_data["status_code"] = response.status_code
            response = Response(response_data, status=response.status_code)

    response = Response(response_data, status=response.status_code)
    return response
