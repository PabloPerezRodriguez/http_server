import get_resource

HTTP_VERSION = 'HTTP/1.0'
PROJECT_NAME = 'pHTTP'

status_codes = {
    200: 'OK',
    403: 'Forbidden',
    404: 'Not Found',
    501: 'Not Implemented'
}
def get_reason(status):
    return status_codes[status]

supported_methods = ['GET']

class Header:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    @staticmethod
    def from_str(string):
        header_list = string.split(': ', 1)
        name, value = header_list
        return Header(name, value)

    def to_str(self):
        return f'{self.name}: {self.value}'


class Request:
    def __init__(self, request_line, headers, body):
        self.request_line = request_line
        self.headers = headers
        self.body = body

    @staticmethod
    def from_str(string):
        lines = string.split('\r\n')

        request_line_str = lines[0]
        headers_str = lines[1:len(lines) - 2]
        body = lines[len(lines) - 1]

        request_line = RequestLine.from_str(request_line_str)
        headers = [Header.from_str(str) for str in headers_str]
        return Request(request_line, headers, body)


class RequestLine:
    def __init__(self, method, resource, http_version):
        self.method = method
        self.resource = resource
        self.http_version = http_version

    @staticmethod
    def from_str(string):
        line_list = string.split(' ')
        method, resource, http_version = line_list
        return RequestLine(method, resource, http_version)


class ResponseLine:
    def __init__(self, status, reason=None, version=None):
        self.status = status

        if reason is None:
            self.reason = get_reason(status)

        if version is None:
            self.version = HTTP_VERSION

    def to_str(self):
        return f'{self.version} {self.status} {self.reason}'


class Response:
    def __init__(self, response_line, headers=None, body=None):
        if headers is None:
            headers = []
        if body is None:
            body = b''

        self.response_line = response_line
        self.headers = headers
        self.body = body

    def add_header(self, header):
        self.headers.append(header)

    def to_bytes(self):
        response_line_str = self.response_line.to_str()
        headers_str = '\r\n'.join([header.to_str() for header in self.headers])

        response_line_bytes = response_line_str.encode(encoding='ASCII')
        headers_bytes = headers_str.encode(encoding='ASCII')
        return response_line_bytes + b'\r\n' + headers_bytes + b'\r\n\r\n' + self.body + b'\r\n'

error_body = '<html lang="en"><head><title>{0}</title></head><body><h1>Error {0}</h1><p>{1}</p></body></html>'
class ErrorResponse(Response):
    def __init__(self, status):
        super().__init__(
            response_line=ResponseLine(status),
            body=b''
        )

        # Get error body from a file
        mime, error = get_resource.get_private(f'errors/{status}.html')

        # If we don't get an error body (because the user hasn't customized their errors), we set a default one
        if not error:
            error = error_body.format(status, get_reason(status)).encode(encoding='ASCII')
            mime = 'text/html'

        self.body = error

        self.add_header(Header('Content-Type', mime))
        self.add_header(Header('Content-Length', len(self.body)))
