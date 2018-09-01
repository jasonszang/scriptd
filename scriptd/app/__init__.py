import logging

from flask import Flask

from scriptd.app.flask_helper import FlaskHelper
from scriptd.app.handler import ScriptdHandler
from scriptd.app.protocol import ScriptdProtocol

app = Flask(__name__)

flask_helper = FlaskHelper(app)
protocol = ScriptdProtocol()
handler = ScriptdHandler(flask_helper, protocol)

log_formatter = logging.Formatter("[pid: %(process)d][tid: %(thread)d][%(levelname)s]" +
                                  "[%(asctime)s][%(filename)s:%(lineno)d] %(message)s")
for h in app.logger.handlers:
    h.setFormatter(log_formatter)
    h.setLevel(logging.INFO)
app.logger.setLevel(logging.INFO)
app.logger.propagate = False

app.add_url_rule("/execute", "execute", handler.handle_execution_request, methods=["POST"])
