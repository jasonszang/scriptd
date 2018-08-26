"""Communication protocol for scriptd"""


class ScriptdProtocol(object):
    """Communication protocol object. Currently a FAKE implementation that is obviously not secure.
    """

    def __init__(self):
        pass

    def generate_token(self):
        """Generate a one-time-use token"""
        # TODO: generate cryptically safe random token, store token
        return "dummy"

    def parse_execution_request(self, request):
        """Parse script execution request, verify authentication and token, then return the command
        requested to execute."""
        # TODO: decrypt, authentication, verify one-time-use token
        command = unicode(request)
        return command

    def emit_response_frame(self, data):
        """Emit one encrypted frame from input data ready to be send to the client."""
        # TODO: encrypt
        frame = str(data)
        return frame
