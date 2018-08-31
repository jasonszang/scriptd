# -*- coding: UTF-8 -*-
"""Helper for working with flask"""

from flask import Flask
from flask import request


class FlaskHelper(object):
    """
    Helper class for interacting with flask framework.
    Improves testability by avoiding accessing flask global/thread-local objects everywhere.
    """

    def __init__(self, app):  # type: (Flask) -> None
        self.app = app

    def get_app(self):  # type: () -> Flask
        return self.app

    def get_request_data(self):  # type: () -> dict
        return request.get_data()
