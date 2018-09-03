# -*- coding: UTF-8 -*-
"""Communication protocol for scriptd"""

import os
import struct
from hashlib import sha256
import threading

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import GCM
from typing import (BinaryIO,
                    Optional,
                    Text)

from scriptd.app.exceptions import AuthenticationError

IV_SIZE = 12
TOKEN_LENGTH = 16
TOKEN_STORAGE_LIMIT = 64
TOKEN_REQUEST_CONTENT = b"TOKEN_REQUEST"


class ScriptdProtocol(object):
    """Communication protocol object. Currently a FAKE implementation that is obviously not secure.
    """

    def __init__(self):
        self._key = None
        self._tokens = set()
        self._tokens_mutex = threading.Lock()

    def set_key(self, key):  # type: (bytes) -> None
        """Set encryption / decryption key. Must be called before using."""
        self._key = sha256(sha256(key).digest() + b"SCRIPTD_SALT").digest()

    def generate_token(self):  # type: () -> bytes
        """Generate a one-time-use token"""
        token = os.urandom(TOKEN_LENGTH)
        with self._tokens_mutex:
            if len(self._tokens) >= TOKEN_STORAGE_LIMIT:
                self._tokens.pop()
            self._tokens.add(token)
        return token

    def parse_execution_request(self, request):  # type: (bytes) -> Text
        """Parse script execution request, verify authentication and token, then return the command
        requested to execute."""
        payload = self.parse_frame(request)
        if len(payload) <= TOKEN_LENGTH:
            raise AuthenticationError("Execution request too short, no token provided?")
        token = payload[:TOKEN_LENGTH]
        with self._tokens_mutex:
            if token not in self._tokens:
                raise AuthenticationError("Invalid token, request retrying "
                                          "or possible replay attack?")
            self._tokens.remove(token)
        command = payload[TOKEN_LENGTH:]
        command = command.decode("UTF-8")
        return command

    def authenticate_token_request(self, request):  # type: (bytes) -> None
        """Decrypts and authenticates one token request."""
        payload = self.parse_frame(request)
        if payload != TOKEN_REQUEST_CONTENT:
            raise AuthenticationError("Incorrect token request content")
        return None

    def emit_frame(self, data, with_size_header=False):  # type: (bytes, bool) -> bytes
        """Emit one encrypted frame from input data ready to be send to the client."""
        iv = os.urandom(IV_SIZE)
        cipher = Cipher(AES(self._key), GCM(iv), default_backend())
        encryptor = cipher.encryptor()
        frame_list = [iv, encryptor.update(data), encryptor.finalize(), encryptor.tag]
        frame = b"".join(frame_list)

        if with_size_header:
            frame = b"".join([struct.pack("!I", len(frame)), frame])
        return frame

    def parse_frame(self, frame):  # type: (bytes) -> bytes
        """Parse one encrypted frame (without size header) and get cleartext data."""
        if len(frame) < IV_SIZE + 16:
            raise AuthenticationError("Frame too short")
        try:
            iv = frame[:IV_SIZE]
            gcm_tag = frame[-16:]
            cipher_text = frame[IV_SIZE:-16]
            cipher = Cipher(AES(self._key), GCM(iv), default_backend())
            decryptor = cipher.decryptor()
            clear_text = decryptor.update(cipher_text) + decryptor.finalize_with_tag(gcm_tag)
            return clear_text
        except InvalidTag:
            raise AuthenticationError("Invalid GCM authentication tag")

    def read_frame_from(self, file_):  # type: (BinaryIO) -> Optional[bytes]
        """Read one encrypted frame from a file-like object which may contain multiple frames."""
        frame_size_binary = file_.read(4)
        if len(frame_size_binary) == 0:
            return None
        frame_size = struct.unpack("!I", frame_size_binary)[0]
        frame = file_.read(frame_size)
        if len(frame) < frame_size:
            raise ValueError("Truncated frame")
        return frame
