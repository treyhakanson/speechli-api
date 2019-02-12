"""Application exception classes."""


class ClientException(Exception):
    """Client exception for invalid API usage."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Constructor."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Serialize the exception to a dictionary."""
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
