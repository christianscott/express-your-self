from expr import *

do([
    re := require('re'),

    for_each := lambda iterable, callback: consume(
        callback(entry) for entry in iterable
    ),

    bisect := lambda iterable, predicate: do([
        front := [],
        back := [],
        flipped := Box(False),

        for_each(iterable, lambda item: do([
            if_then(
                not flipped.get(),
                lambda: flipped.set(lambda _: predicate(item)),
            ),
            (back if flipped.get() else front).append(item),
        ])),

        (front, back),
    ]),

    Header := t('Header', ['name', 'value']),

    parse_header := lambda header: do([
        split_header := re.split(': ', header),
        Header(split_header[0], split_header[1])
    ]),

    Request := t('Request', [
        'method',
        'path',
        'headers',
        'body',
    ]),

    parse := lambda message: do([
        lines := re.split('\r?\n', message),

        split_message := bisect(lines, lambda line: line == ""),

        message_header := split_message[0],
        message_body := "\n".join(split_message[1]),
        
        request_line := message_header[0].split(' '),
        method := request_line[0],
        path := request_line[1],

        headers := [] if len(message_header) == 1 else \
            [parse_header(header) for header in message_header[1:] if len(header)],

        Request(method, path, headers, body),
    ]),

    export(__name__, parse)
])
