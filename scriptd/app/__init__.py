import logging

from flask import Flask

from scriptd.app.flask_helper import FlaskHelper
from scriptd.app.handler import ScriptdHandler
from scriptd.app.protocol import ScriptdProtocol

app = Flask(__name__)

flask_helper_ = FlaskHelper(app)
protocol_ = ScriptdProtocol()
handler_ = ScriptdHandler(flask_helper_, protocol_)

log_formatter = logging.Formatter("[pid: %(process)d][tid: %(thread)d][%(levelname)s]" +
                                  "[%(asctime)s][%(filename)s:%(lineno)d] %(message)s")
for h in app.logger.handlers:
    h.setFormatter(log_formatter)
    h.setLevel(logging.INFO)
app.logger.setLevel(logging.INFO)
app.logger.propagate = False

app.add_url_rule("/execute", "execute", handler_.handle_execution_request, methods=["POST"])
app.add_url_rule("/token", "token", handler_.handle_token_request, methods=["POST"])
