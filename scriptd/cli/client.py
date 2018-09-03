# -*- coding: UTF-8 -*-
"""Client CLI entrypoint"""

import argparse
import sys

import requests
import six

from scriptd.app import util
from scriptd.app.exceptions import AuthenticationError
from scriptd.app.protocol import ScriptdProtocol


def main():
    argparser = argparse.ArgumentParser(description="Scriptd client")
    argparser.add_argument("-H", "--host", type=six.text_type, default=u"localhost",
                           help="Server ip or name, default: localhost")
    argparser.add_argument("-p", "--port", type=int, default=u"8182",
                           help="Server port, default: 8182")
    key_group = argparser.add_mutually_exclusive_group(required=False)
    key_group.add_argument("-k", "--key", type=six.text_type, default=u"",
                           help="Authentication key, default: empty")
    key_group.add_argument("--key-file", type=six.text_type,
                           help="Authentication key file. Its salted hash will be used as key.")
    argparser.add_argument("command", type=six.text_type,
                           help="Name of the script to run on server")

    args = argparser.parse_args()

    if args.key_file is not None:
        key = util.derive_key_from_key_file(args.key_file)
    else:
        key = args.key.encode("UTF-8")

    protocol = ScriptdProtocol()
    protocol.set_key(key)

    resp = requests.post("http://{}:{}/execute".format(args.host, args.port),
                         data=protocol.emit_frame(args.command.encode("UTF-8")),
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
        six.print_("Authentication failed, fake server?", file=sys.stderr)
    if response_empty:
        six.print_("Empty response, incorrect key or invalid server?", file=sys.stderr)


if __name__ == "__main__":
    main()
