#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
import psycopg2


def create_app():
    from .blueprints import generate

    app = Flask(__name__)
    app.register_blueprint(generate)

    app.dbconn = psycopg2.connect('dbname=default host=postgres')

    return app
