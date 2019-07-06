import threading, select, classes
from classes import *
from get_resource import get_resource

timeout_in_seconds = 0.1


class ClientThread(threading.Thread):
    def __init__(self, ip, port, socket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.socket = socket

    def run(self):
        received_data = self.parse()
        # turn bytes into string
        received_str = received_data.decode(encoding='ASCII')

        # get request object from string
        request = Request.from_str(received_str)
        response = None

        request_line = request.request_line
        headers = request.headers
        # get method
        if request_line.method in classes.supported_methods:
            if request_line.method == 'GET':
                response = None
                print(f'GET {request_line.resource} {self.ip}')
                try:
                    mime_type, body = get_resource(request_line.resource)

                    content_length = len(body)

                    response = Response(
                        response_line=ResponseLine(status=200),
                        headers=[
                            Header('Content-Type', mime_type),
                            Header('Content-Length', content_length)
                        ],
                        body=body
                    )
                except FileNotFoundError as e:
                    print('404')
                    response = ErrorResponse(status=404)
                except PermissionError as e:
                    print('403')
                    response = ErrorResponse(status=403)
            elif request_line.method == 'POST':
                print(f'POST {request_line.resource} {self.ip}')
                content_type = any(header.name == 'Content-Type' for header in headers)
                if content_type:
                    # TODO: POST
                    print('POST')

        else:
            print('Unknown Method')
            ErrorResponse(status=501)
            print(f'Received unknown method {request_line.method}')

        response.add_header(Header('X-Server', PROJECT_NAME))
        self.socket.send(response.to_bytes())
        self.socket.close()

    def parse(self):
        received_data = bytes()

        while True:
            # Check if socket can receive data
            ready, _, _ = select.select([self.socket], [], [], timeout_in_seconds)

            if ready:
                # If it can, receive it
                data = self.socket.recv(16)

                received_data += data
            else:
                return received_data