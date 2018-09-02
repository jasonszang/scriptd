# -*- coding: UTF-8 -*-
"""Client CLI entrypoint"""

import argparse
import sys

import requests
import six

from scriptd.app.exceptions import AuthenticationError
from scriptd.app.protocol import ScriptdProtocol


def main():
    argparser = argparse.ArgumentParser(description="Scriptd client")
    argparser.add_argument("host", type=six.text_type, help="Host ip or name")
    argparser.add_argument("port", type=int, help="Host port")
    argparser.add_argument("key", type=six.text_type, help="Authentication key")
    argparser.add_argument("command", type=six.text_type,
                           help="Name of the script to run on server")

    args = argparser.parse_args()
    host = args.host
    port = args.port
    cmd = args.command
    key = args.key.encode("UTF-8")

    protocol = ScriptdProtocol()
    protocol.set_key(key)

    resp = requests.post("http://{}:{}/execute".format(host, port),
                         data=protocol.emit_frame(cmd.encode("UTF-8")),
                         stream=True)

    response_empty = True
    try:
        while True:
            frame = protocol.read_frame_from(resp.raw)
            if frame is None:
                break
            frame_data = protocol.parse_frame(frame)
            if six.PY3:
                sys.stdout.buffer.write(frame_data)
            else:
                sys.stdout.write(frame_data)
            response_empty = False
    except AuthenticationError:
        six.print_("Authentication failed, fake server?")
    if response_empty:
        six.print_("Empty response, incorrect key or invalid server?")


if __name__ == "__main__":
    main()
