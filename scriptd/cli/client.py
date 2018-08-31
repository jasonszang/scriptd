# -*- coding: UTF-8 -*-
"""Client CLI entrypoint"""

import argparse

import requests
from six import print_


def main():
    argparser = argparse.ArgumentParser(description="Scriptd client")
    argparser.add_argument("host", type=str, help="Host ip or name")
    argparser.add_argument("port", type=int, help="Host port")
    argparser.add_argument("command", type=str, help="Name of the script to run on server")

    args = argparser.parse_args()
    host = args.host
    port = args.port
    cmd = args.command

    resp = requests.post("http://{}:{}/execute".format(host, port), data=cmd)
    print_(resp.content)


if __name__ == "__main__":
    main()
