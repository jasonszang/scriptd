# -*- coding: UTF-8 -*-
"""Miscellaneous utilities"""

from hashlib import sha256

from typing import Text


def derive_key_from_key_file(key_file_path):  # type: (Text) -> bytes
    with open(key_file_path, "rb") as fin:
        digest = sha256()
        while True:
            block = fin.read(65536)
            if len(block) == 0:
                break
            digest.update(block)
    return digest.digest()
