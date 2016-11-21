# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from datetime import date
from django.contrib import auth
from django.contrib.auth.models import User
from django.conf import  settings
from .serializers import HttpLogSerializer
from rest_framework.response import Response


def get_request_ip(request):
    if request.META is 'HTTP_X_FORWARDED_FOR':
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']


def get_client_data(request):
    return {
        'ip': get_request_ip(request),
    }


def get_server_data(request):
    server = request.META['HTTP_HOST'].split(':')

    return {
        'host': server[0],
        'port': server[1],
    }


def get_request_data(request):
    return {
        'method': request.method,
        'path': request.path,
        'data': json.loads(request.body),
    }


def get_httplog_data(request):
    return {
        'client': get_client_data(request),
        'server': get_server_data(request),
        'request': get_request_data(request),
    }


def save_request_data(request_data, request):
    serializer = HttpLogSerializer(data=request_data, partial=True)

    if serializer.is_valid():
        user = User.objects.get(id=request.user.id)
        return serializer.save(user=user)


def get_response_data(response):
    if isinstance(response, Response):
        return {
            'status_code': response.status_code,
            'data': response.data,
        }
    else:
        return {}


def save_response_data(api_info, response_data):
    api_info.response = response_data
    api_info.save(update_fields=['response'])


def get_es_log_data(request_data, response_data, user):
    request_data['response'] = response_data
    return request_data


def get_hostname():
    return settings.REST_CLIENT_SETTINGS['ES']['default']['HOSTNAME']


def get_port():
    return settings.REST_CLIENT_SETTINGS['ES']['default']['PORT']


def set_es_url():
    return '{}:{}'.format(get_hostname(), get_port())


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = auth.get_user(request)
    return request._cached_user
