# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField


class HttpLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    client = JSONField(default={}, null=True, blank=True)
    server = JSONField(default={}, null=True, blank=True)
    request = JSONField(default={}, null=True, blank=True)
    response = JSONField(default={}, null=True, blank=True)
    user = models.ForeignKey(
        User, related_name='httplogs', db_constraint=False, null=True)

    class Meta:
        db_table = 'http_log'
