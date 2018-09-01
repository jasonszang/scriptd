# -*- coding: UTF-8 -*-
"""Client CLI entrypoint"""

import argparse

import requests
import six

from scriptd.app.protocol import ScriptdProtocol


def main():
    argparser = argparse.ArgumentParser(description="Scriptd client")
    argparser.add_argument("host", type=six.text_type, help="Host ip or name")
    argparser.add_argument("port", type=int, help="Host port")
    argparser.add_argument("command", type=six.text_type,
                           help="Name of the script to run on server")

    args = argparser.parse_args()
    host = args.host
    port = args.port
    cmd = args.command

    protocol = ScriptdProtocol()

    resp = requests.post("http://{}:{}/execute".format(host, port),
                         data=protocol.emit_frame(cmd.encode("UTF-8")))
    six.print_(resp.content)


if __name__ == "__main__":
    main()
