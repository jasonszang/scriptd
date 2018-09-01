# -*- coding: UTF-8 -*-
"""Communication protocol for scriptd"""

import six
from typing import Text


class ScriptdProtocol(object):
    """Communication protocol object. Currently a FAKE implementation that is obviously not secure.
    """

    def __init__(self):
        pass

    def generate_token(self):  # type: () -> bytes
        """Generate a one-time-use token"""
        # TODO: generate cryptically safe random token, store token
        return b"dummy"

    def parse_execution_request(self, request):  # type: (bytes) -> Text
        """Parse script execution request, verify authentication and token, then return the command
        requested to execute."""
        # TODO: decrypt, authentication, verify one-time-use token
        command = request.decode("UTF-8")
        return command

    def emit_frame(self, data):  # type: (bytes) -> bytes
        """Emit one encrypted frame from input data ready to be send to the client."""
        # TODO: encrypt
        if not isinstance(data, six.binary_type):
            raise TypeError("Expect binary, got {}".format(type(data).__name__))
        frame = str(data)
        return frame
