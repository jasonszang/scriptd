from __future__ import print_function

from flask import Flask

from scriptd.app.flask_helper import FlaskHelper
from scriptd.app.handler import ScriptdHandler
from scriptd.app.protocol import ScriptdProtocol

app = Flask(__name__)

flask_helper = FlaskHelper(app)
protocol = ScriptdProtocol()
handler = ScriptdHandler(flask_helper, protocol)

app.add_url_rule("/execute", "execute", handler.handle_execution_request, methods=["POST"])
