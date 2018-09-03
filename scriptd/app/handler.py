# -*- coding: UTF-8 -*-
"""Request handler"""
import os
import subprocess

import six
from flask import Response
from typing import Text

from scriptd.app.exceptions import (AuthenticationError,
                                    ScriptdError,
                                    NoSuchScriptError,
                                    NotPermittedError)
from scriptd.app.flask_helper import FlaskHelper
from scriptd.app.protocol import ScriptdProtocol


class ScriptdHandler(object):
    def __init__(self, flask_helper, protocol):  # type: (FlaskHelper, ScriptdProtocol) -> None
        self._fh = flask_helper
        self._pr = protocol
        self._working_dir = u"."
        self._logger = self._fh.get_logger()

    def set_working_dir(self, working_dir):  # type: (Text) -> None
        if not isinstance(working_dir, six.text_type):
            raise TypeError("Expect unicode, got {}".format(type(working_dir).__name__))
        self._working_dir = working_dir
        return None

    def handle_execution_request(self):  # type: () -> Response
        try:
            self._logger.info("Accept request from: {}".format(self._fh.get_remote_addr()))
            req = self._fh.get_request_data()
            command = self._pr.parse_execution_request(req)
            if "/" in command or "\\" in command:
                raise NotPermittedError("Scripts in subdirectories are not allowed")
            if command not in os.listdir(self._working_dir):
                raise NoSuchScriptError("No such script")
            if not os.access(command, os.X_OK):
                raise NotPermittedError("File has no execution permission")
            self._logger.info("Executing command \"{}\" upon request from: {}"
                              .format(command, self._fh.get_remote_addr()))
            return self._do_execution(command)
        except AuthenticationError as e:
            self._logger.info("Request authentication failed: {}".format(str(e)))
            return Response("", status=403)
        except ScriptdError as e:
            self._logger.info("Rejected execution request: {}".format(str(e)))
            return Response(self._pr.emit_frame(six.binary_type(e), with_size_header=True))
        except Exception as e:
            self._logger.info("Caught unexpected exception: {}".format(str(e)))
            return Response("", status=500)

    def _do_execution(self, command):  # type: (Text) -> Response
        try:
            subp = subprocess.Popen([os.path.join(self._working_dir, command)],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    cwd=self._working_dir)
        except WindowsError:  # os.access with X_OK does not work on Windows
            raise NotPermittedError("File cannot be executed on Windows")

        def gen():
            while True:
                subp.poll()
                chunk_size = 64 if subp.returncode is None else -1
                dat = subp.stdout.read(chunk_size)
                if len(dat) > 0:
                    yield self._pr.emit_frame(dat, with_size_header=True)
                if subp.returncode is not None:
                    break

        return Response(gen(), mimetype="application/octet-stream")

    def handle_token_request(self):  # type: () -> Response
        try:
            self._logger.info("Accept token request from: {}".format(self._fh.get_remote_addr()))
            req = self._fh.get_request_data()
            self._pr.authenticate_token_request(req)
            token = self._pr.generate_token()
            return Response(self._pr.emit_frame(token))
        except AuthenticationError as e:
            self._logger.info("Request authentication failed: {}".format(str(e)))
            return Response("", status=403)
        except Exception as e:
            self._logger.info("Caught unexpected exception: {}".format(str(e)))
            return Response("", status=500)
