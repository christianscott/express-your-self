from expr import *

do([
    re := require('re'),

    for_each := lambda iterable, callback: consume(
        callback(entry) for entry in iterable
    ),

    Header := t('Header', ['name', 'value']),

    parse_header := lambda header: do([
        split_header := re.split(': ', header),
        Header(split_header[0], split_header[1])
    ]),

    Request := t('Request', [
        'method',
        'path',
        'headers',
    ]),

    parse := lambda message: do([
        lines := re.split('\r?\n', message),
        
        request_line := lines[0].split(' '),
        method := request_line[0],
        path := request_line[1],

        headers := [] if len(lines) == 1 else \
            [parse_header(header) for header in lines[1:] if len(header)],

        Request(method, path, headers),
    ]),

    export(__name__, parse)
])
