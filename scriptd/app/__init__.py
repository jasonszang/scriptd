from __future__ import print_function

from flask import Flask

from flask_helper import FlaskHelper
from handler import ScriptdHandler
from protocol import ScriptdProtocol

app = Flask(__name__)

flask_helper = FlaskHelper(app)
protocol = ScriptdProtocol()
handler = ScriptdHandler(flask_helper, protocol)

app.add_url_rule("/execute", "execute", handler.handle_execution_request, methods=["POST"])
