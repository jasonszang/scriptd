# -*- coding: UTF-8 -*-
"""Communication protocol for scriptd"""

import struct
from typing import (BinaryIO,
                    Optional,
                    Text)


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
        payload = self.parse_frame(request)
        command = payload.decode("UTF-8")
        return command

    def emit_frame(self, data, with_size_header=False):  # type: (bytes, bool) -> bytes
        """Emit one encrypted frame from input data ready to be send to the client."""
        # TODO: encrypt
        frame = str(data)
        if with_size_header:
            frame = "".join([struct.pack("!I", len(frame)), frame])
        return frame

    def parse_frame(self, frame):  # type: (bytes) -> bytes
        """Parse one encrypted frame and get cleartext data."""
        # TODO: decrypt
        data = str(frame)
        return data

    def read_frame_from(self, file_):  # type: (BinaryIO) -> Optional[bytes]
        """Read one encrypted frame from a file-like object which may contain multiple frames."""
        frame_size_binary = file_.read(4)
        if frame_size_binary == "":
            return None
        frame_size = struct.unpack("!I", frame_size_binary)[0]
        frame = file_.read(frame_size)
        if len(frame) < frame_size:
            raise ValueError("Truncated frame")
        return frame
