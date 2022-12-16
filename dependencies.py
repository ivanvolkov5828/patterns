from quopri import decodestring

# for GET
# --------------------------------------------------------------------
def parse_input_data(data: str):
    result = {}
    if data:
        params = data.split('&')
        for item in params:
            key, value = item.split('=')
            result[key] = value
    return result

def get_request_params(environ):
    query_string = environ['QUERY_STRING']
    request_params = parse_input_data(query_string)
    return request_params
# --------------------------------------------------------------------

# for POST
# --------------------------------------------------------------------
def post_parse_input_data(data: str):
    result = {}
    if data:
        params = data.replace('\r\n','').replace(' ', '') \
            .replace('{', '').replace('}', '').replace('"', '').split(',')

        for item in params:
            key, value = item.split(':')
            result[key] = value
    return result


def get_wsgi_input_data(env) -> bytes:
    content_length_data = env.get('CONTENT_LENGTH')
    content_length = int(content_length_data) if content_length_data else 0
    data = env['wsgi.input'].read(content_length) \
        if content_length > 0 else b''
    return data

def parse_wsgi_input_data(data: bytes) -> dict:
    result = {}
    if data:
        data_str = data.decode(encoding='utf-8')
        result = post_parse_input_data(data_str)
    return result


def post_get_request_params(environ):
    data = get_wsgi_input_data(environ)
    data = parse_wsgi_input_data(data)
    return data
# --------------------------------------------------------------------


# for normal data display
def decode_value(data):
    new_data = {}
    for key, value in data.items():
        val = bytes(value.replace('%', '=').replace('+', " "), 'UTF-8')
        val_decode_str = decodestring(val).decode('UTF-8')
        new_data[key] = val_decode_str
    return new_data
