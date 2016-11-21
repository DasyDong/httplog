# -*- coding: utf-8 -*-
from rest_framework import viewsets

from .filters import HttpLogFilter

from .serializers import HttpLogSerializer
from .models.httplog import HttpLog


class HttpLogViewSet(viewsets.ModelViewSet):
    queryset = HttpLog.objects.all().order_by('id')
    serializer_class = HttpLogSerializer
    filter_class = HttpLogFilter
