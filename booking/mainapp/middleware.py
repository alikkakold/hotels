# coding:utf-8
import sys
import traceback

from django.http import HttpResponseServerError
from django.template import loader
from django.urls import resolve

from booking import settings
from supportapp.models import RequestException


class ExceptionHandlerMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print(response)
        print(request.path_info)

        if settings.HANDLE_EXCEPTION:
            if response.status_code >= 404:
                type, value, tb = sys.exc_info()

                RequestException.objects.create(page=request.path_info,
                                                exception_text=traceback.format_exception(type, value, tb),
                                                status_code=404,
                                                user=request.user)

            if response.status_code == 404:
                print(response.status_code)
                template = loader.get_template('mainapp/404.html')
                return HttpResponseServerError(template.render())

            elif response.status_code == 500:
                print(response.status_code)
                template = loader.get_template('mainapp/500.html')
                return HttpResponseServerError(template.render())

        return response
