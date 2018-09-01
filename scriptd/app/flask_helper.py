# -*- coding: UTF-8 -*-
"""Helper for working with flask"""
import logging

from flask import Flask
from flask import request
from typing import Text


class FlaskHelper(object):
    """
    Helper class for interacting with flask framework.
    Improves testability by avoiding accessing flask global/thread-local objects everywhere.
    """

    def __init__(self, app):  # type: (Flask) -> None
        self.app = app

    def get_app(self):  # type: () -> Flask
        return self.app

    def get_logger(self):  # type: () -> logging.Logger
        return self.app.logger

    def get_request_data(self):  # type: () -> bytes
        return request.get_data()

    def get_remote_addr(self):  # type: () -> Text
        return request.remote_addr
