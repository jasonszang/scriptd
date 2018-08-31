# -*- coding: UTF-8 -*-
"""Server CLI entrypoint"""
import argparse

from flask import Flask

from scriptd.app import app


def main():
    argparser = argparse.ArgumentParser(description="Scriptd server")
    argparser.add_argument("-H", "--host", type=str, default="0.0.0.0",
                           help="Host name to listen on, default: 0.0.0.0")
    argparser.add_argument("-p", "--port", type=int, default=8182,
                           help="Port to listen on, default: 8182")
    args = argparser.parse_args()
    host = args.host
    port = args.port
    Flask.run(app, host, port, threaded=True)


if __name__ == "__main__":
    main()
