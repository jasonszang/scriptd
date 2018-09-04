# -*- coding: UTF-8 -*-
"""Server CLI entrypoint"""
import argparse

import six
from flask import Flask

from scriptd.app import app
from scriptd.app import handler_
from scriptd.app import protocol_
from scriptd.app import util


def main():
    argparser = argparse.ArgumentParser(description="Scriptd server")
    argparser.add_argument("-H", "--host", type=six.text_type, default=u"0.0.0.0",
                           help="Host name to listen on, default: 0.0.0.0")
    argparser.add_argument("-p", "--port", type=int, default=u"8182",
                           help="Port to listen on, default: 8182")
    key_group = argparser.add_mutually_exclusive_group(required=False)
    key_group.add_argument("-k", "--key", type=six.text_type, default=u"",
                           help="Authentication key, default: empty")
    key_group.add_argument("--key-file", type=six.text_type,
                           help="Authentication key file. Key will be derived from its hash.")
    argparser.add_argument("-d", "--dir", type=six.text_type, default=u".",
                           help="Working directory, default: current dir")

    args = argparser.parse_args()

    if args.key_file is not None:
        key = util.derive_key_from_key_file(args.key_file)
    else:
        key = args.key.encode("UTF-8")
    protocol_.set_key(key)
    handler_.set_working_dir(args.dir)
    # XXX: pass these parameters before initing app so that these can be set var constructor

    Flask.run(app, args.host, args.port, threaded=True)


if __name__ == "__main__":
    main()
