# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
from datetime import date
from django.forms import model_to_dict
from .services import set_es_url

from elasticsearch import Elasticsearch

from celery import shared_task


@shared_task(serializer='json')
def task_user_behavior(es_log_data):

    body = json.dumps(model_to_dict(es_log_data))

    es = Elasticsearch(set_es_url())
    es.index(index='cd_event_log_{}'.format(date.today()),doc_type='log',body=body)
