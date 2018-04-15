#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask


def create_app():
    from .blueprints import generate

    app = Flask(__name__)
    app.register_blueprint(generate)

    return app
