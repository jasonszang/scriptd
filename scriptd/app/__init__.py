from __future__ import print_function

import subprocess
import sys

from flask import Flask
from flask import Response
from flask import request
from flask_helper import FlaskHelper
from protocol import ScriptdProtocol
from handler import ScriptdHandler

app = Flask(__name__)

flask_helper = FlaskHelper(app)
protocol = ScriptdProtocol()
handler = ScriptdHandler(flask_helper, protocol)

app.add_url_rule("/execute", "execute", handler.handle_execution_request, methods=["POST"])
