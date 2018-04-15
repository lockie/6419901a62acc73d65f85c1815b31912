#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http import HTTPStatus

from flask import Blueprint, request, abort, Response
import requests


generate = Blueprint('generate', __name__)


@generate.route('/generate', methods=['POST'])
def generate_graph():
    series = request.get_json()
    return Response(do_generate_graph(series), content_type='image/png')


def do_generate_graph(series):
    res = requests.post(
        'http://highcharts:8080', stream=True,
        json={
            'infile': {
                'chart': {
                    'type': 'spline'
                },
                'plotOptions': {
                    'spline': {
                        'marker': {
                            'enabled': None
                        }
                    }
                },
                'title': {
                    'text': ''
                },
                'xAxis': {
                    'type': 'datetime',
                    'title': {
                        'text': 't'
                    }
                },
                'yAxis': {
                    'type': 'linear',
                    'title': {
                        'text': 'y'
                    }
                },
                'series': [{
                    'name': 'f(t)',
                    'data': [[int(t * 1000), f] for t, f in series]
                }]
            }
        })
    if res.status_code != HTTPStatus.OK:
        abort(res.status_code)
    return res.raw.read()
