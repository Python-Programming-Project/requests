import http.client
import urllib.parse
from urllib.parse import urlparse
import json as _json
from .response import Response


def send_request(method, url, body=None, headers=None, **kwargs):
    print(f"sending {method} request to {url} via custom requests module")
    headers = headers or {}
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path + '?' + \
        parsed_url.query if parsed_url.query else parsed_url.path

    conn = http.client.HTTPConnection(
        host) if parsed_url.scheme == 'http' else http.client.HTTPSConnection(host)

    conn.request(method, path, body=body, headers=headers)
    response = conn.getresponse()
    wrapped_response = Response(response)

    allow_redirects = kwargs.get('allow_redirects', True)
    max_redirects = kwargs.get('max_redirects', 5)
    current_redirects = kwargs.get('current_redirects', 0)
    if allow_redirects and 300 <= wrapped_response.status < 400 and current_redirects < max_redirects:
        location = wrapped_response.headers.get('Location')
        if location:
            parsed_url = urlparse(location)
            if not parsed_url.netloc:
                location = urllib.parse.urljoin(url, location)
            print(f"Redirecting to {location}")
            return send_request(method, location, body=body, headers=headers, max_redirects=max_redirects, current_redirects=current_redirects + 1)

    return wrapped_response


def get(url, params=None, **kwargs):
    if params:
        url += '?' + urllib.parse.urlencode(params)
    return send_request('GET', url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    headers = {}
    body = None
    if data:
        body = urllib.parse.urlencode(data)
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    if json:
        body = _json.dumps(json)
        headers['Content-Type'] = 'application/json'
    return send_request('POST', url, body=body, headers=headers, **kwargs)
