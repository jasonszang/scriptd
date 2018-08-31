# -*- coding: UTF-8 -*-
"""Request handler"""
from __future__ import print_function

import os
import subprocess

from flask import Response

from scriptd.app.exceptions import (ScriptdError,
                                    NoSuchScriptError,
                                    NotPermittedError)
from scriptd.app.flask_helper import FlaskHelper
from scriptd.app.protocol import ScriptdProtocol


class ScriptdHandler(object):
    def __init__(self, flask_helper, protocol):  # type: (FlaskHelper, ScriptdProtocol) -> None
        self._fh = flask_helper
        self._pr = protocol

    def handle_execution_request(self):
        try:
            req = self._fh.get_request_data()
            command = self._pr.parse_execution_request(req)
            if "/" in command or "\\" in command:
                raise NotPermittedError("Scripts in subdirectories are not allowed")
            if command not in os.listdir(u"."):
                raise NoSuchScriptError("No such script")
            if not os.access(command, os.X_OK):
                raise NotPermittedError("File has no execution permission")
            return self._do_execution(command)
        except ScriptdError as e:
            return self._pr.emit_response_frame(str(e))

    def _do_execution(self, command):
        try:
            subp = subprocess.Popen([os.path.join(".", command)], stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        except WindowsError:  # os.access with X_OK does not work on Windows
            raise NotPermittedError("File cannot be executed on windows")

        def gen():
            while True:
                subp.poll()
                chunk_size = 64 if subp.returncode is None else -1
                dat = subp.stdout.read(chunk_size)
                if len(dat) > 0:
                    yield self._pr.emit_response_frame(dat)
                if subp.returncode is not None:
                    return

        return Response(gen(), mimetype="text/plain")
