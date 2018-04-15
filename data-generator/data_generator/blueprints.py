#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http import HTTPStatus

from flask import Blueprint, current_app, request, abort, Response
from psycopg2 import DatabaseError


generate = Blueprint('generate', __name__)


@generate.route('/generate', methods=['POST'])
def generate_data():
    data = request.get_json()
    try:
        function = data['function']
        interval = int(data['interval'])
        dt = int(data['dt'])
    except (KeyError, ValueError):
        abort(HTTPStatus.BAD_REQUEST)
    return Response(str(do_generate_data(function, interval, dt)),
                    content_type='application/json; charset=utf-8')


non_allowed_chars = ';'


def do_generate_data(function, interval, dt):
    ''' Fulfill the most weird technical requirement I've seen in years '''

    if any(char in non_allowed_chars for char in function):
        abort(HTTPStatus.BAD_REQUEST)

    with current_app.dbconn.cursor() as cursor:
        try:
            cursor.execute('''select t, {} as f from (
            select (extract(epoch from times)) as t from
            generate_series(statement_timestamp() - interval '%s days',
            statement_timestamp(),
            '%s hours') as times) as timeseries
            '''.format(function),  # NOTE : still a potential security breach
                        (interval, dt))
        except DatabaseError:
            cursor.execute('rollback')
            abort(HTTPStatus.BAD_REQUEST)
        return [[row[0], row[1]] for row in cursor.fetchall()]
