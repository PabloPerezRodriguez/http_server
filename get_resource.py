import os
import magic

def get_resource(resource):
    # TODO: Prevent exploitation with resource='../'
    resource_relpath = os.path.relpath(resource, '/')

    path = os.path.join('./public', resource_relpath)
    if os.path.isfile(path) and os.path.exists(path) and not os.path.islink(path):
        try:
            with open(path, 'rb') as f:
                mime_type = magic.from_file(path, mime=True)
                body = f.read()
                return mime_type, body
        except PermissionError as e:
            raise PermissionError()

    elif resource == '/':
        # / -> /index.html
        return get_resource('/index.html')
    else:
        raise FileNotFoundError()

def get_private(file):
    # TODO: Prevent exploitation with file='../'
    path = os.path.join('./private', file)
    if os.path.isfile(path) and os.path.exists(path) and not os.path.islink(path):
        try:
            with open(path, 'rb') as f:
                mime_type = magic.from_file(path, mime=True)
                body = f.read()
                return mime_type, body
        except PermissionError as e:
            return None, None
    else:
        return None, None
