# -*- coding: UTF-8 -*-
"""Server CLI entrypoint"""

from flask import Flask
from scriptd.app import app


def main():
    # TODO: command line cli
    Flask.run(app, "localhost", 8182, threaded=True)


if __name__ == "__main__":
    main()
