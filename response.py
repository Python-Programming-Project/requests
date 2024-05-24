import json
from http.client import HTTPResponse


class Response:
    def __init__(self, http_response: HTTPResponse):
        self._response = http_response
        self._content = None
        self._json = None

    @property
    def status_code(self):
        return self._response.status

    @property
    def headers(self):
        return dict(self._response.getheaders())

    @property
    def content(self):
        if self._content is None:
            self._content = self._response.read()
        return self._content

    @property
    def text(self):
        return self.content.decode('utf-8')

    def json(self):
        if self._json is None:
            self._json = json.loads(self.text)
        return self._json

    def close(self):
        self._response.close()
