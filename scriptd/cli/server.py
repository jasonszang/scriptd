# -*- coding: UTF-8 -*-
"""Server CLI entrypoint"""
import argparse
import six

from flask import Flask

from scriptd.app import app
from scriptd.app import handler


def main():
    argparser = argparse.ArgumentParser(description="Scriptd server")
    argparser.add_argument("-H", "--host", type=six.text_type, default=u"0.0.0.0",
                           help="Host name to listen on, default: 0.0.0.0")
    argparser.add_argument("-p", "--port", type=six.text_type, default=u"8182",
                           help="Port to listen on, default: 8182")
    argparser.add_argument("-d", "--dir", type=six.text_type, help="Working directory")
    args = argparser.parse_args()
    host = args.host
    port = args.port
    working_dir = args.dir
    if working_dir is not None:
        handler.set_working_dir(working_dir)

    Flask.run(app, host, port, threaded=True)


if __name__ == "__main__":
    main()
