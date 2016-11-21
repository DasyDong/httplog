# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.conf import settings
from django.utils.functional import SimpleLazyObject
from importlib import import_module

from .services import get_request_data, save_request_data, get_es_log_data, get_user, get_response_data, save_response_data
from .tasks import task_user_behavior


class UserBehaviorExtractMiddleware(object):

    def __init__(self):
        self.engine = import_module(settings.SESSION_ENGINE)

    def __call__(self):
        self.http_log = None
        self.request_data = None

    def set_session(self, request):
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        request.session = self.engine.SessionStore(session_key)
        request.user = SimpleLazyObject(lambda: get_user(request))

    def is_valid_method(self, request):
        return request.method in settings.USER_BEHAVIOR_CONFIG['METHODS']

    def is_valid_url(self, request):
        return request.path in settings.USER_BEHAVIOR_CONFIG['PERMITTED_URLS']

    def is_valid_user(self, request):
        return hasattr(request, 'user') and request.user.id

    def is_valid_config(self):
        return hasattr(settings, 'USER_BEHAVIOR_CONFIG')

    def is_log_to_db(self):
        return settings.USER_BEHAVIOR_CONFIG['LOG_TO_DB']

    def is_log_to_es(self):
        return settings.USER_BEHAVIOR_CONFIG['LOG_TO_ES']

    def process_request(self, request):
        self.set_session(request)

        if self.is_valid_method(request) and self.is_valid_url(request) and self.is_valid_user(request):
            request_data = get_request_data(request)
            self.request_data = request_data

            if self.is_valid_config() and self.is_log_to_db():
                self.http_log = save_request_data(self.request_data, request)

    def process_response(self, request, response):
        if self.is_valid_method(request) and self.is_valid_url(request) and self.is_valid_user(request):
            response_data = get_response_data(response)

            if self.is_valid_config() and self.is_log_to_db():
                save_response_data(self.http_log, response_data)

            if self.is_valid_config() and self.is_log_to_es():
                es_log_data = get_es_log_data(self.request_data, response_data, request.user)
                task_user_behavior(es_log_data)

        return response
