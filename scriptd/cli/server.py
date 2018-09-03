# -*- coding: UTF-8 -*-
"""Server CLI entrypoint"""
import argparse
import six

from flask import Flask

from scriptd.app import app
from scriptd.app import protocol
from scriptd.app import handler


def main():
    argparser = argparse.ArgumentParser(description="Scriptd server")
    argparser.add_argument("-H", "--host", type=six.text_type, default=u"0.0.0.0",
                           help="Host name to listen on, default: 0.0.0.0")
    argparser.add_argument("-p", "--port", type=int, default=u"8182",
                           help="Port to listen on, default: 8182")
    argparser.add_argument("-k", "--key", type=six.text_type, default=u"",
                           help="Authentication key, default: empty")
    argparser.add_argument("-d", "--dir", type=six.text_type, default=u".",
                           help="Working directory, default: current dir")
    # TODO: key file instead of cmd line only
    args = argparser.parse_args()
    host = args.host
    port = args.port
    working_dir = args.dir
    key = args.key.encode("UTF-8")
    protocol.set_key(key)
    handler.set_working_dir(working_dir)
    # XXX: pass these parameters before initing app so that these can be set var constructor

    Flask.run(app, host, port, threaded=True)


if __name__ == "__main__":
    main()
