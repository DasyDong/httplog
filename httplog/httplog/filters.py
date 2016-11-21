# -*- coding: utf-8 -*-
import django_filters
from django_filters.filters import MethodFilter

from django.contrib.auth.models import User
from .models.httplog import HttpLog


class HttpLogFilter(django_filters.FilterSet):
    user = MethodFilter(action='user_filter')
    status_code = MethodFilter(action='status_code_filter')

    class Meta:
        model = HttpLog
        fields = ('user', 'status_code')

    @classmethod
    def user_filter(cls, queryset, username):
        return queryset.filter(user__username__contains=username)

    @classmethod
    def status_code_filter(cls, queryset, status_code):
        id_list = []
        for qs in queryset:
            if qs.response.has_key('status_code'):
                if qs.response['status_code'] == int(status_code):
                    id_list.append(qs.id)
        return queryset.filter(id__in=id_list)
