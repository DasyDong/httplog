# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from rest_framework import routers

from .views import HttpLogViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'httplog', HttpLogViewSet)

url_patterns = [
    url(r'', include(router.urls)),
]
