from expr import *

do([
    re := require('re'),

    bisect := lambda iterable, predicate: do([
        front := [],
        back := [],
        has_flipped := Box(False),

        for_each(iterable, lambda item: do([
            if_then(
                not has_flipped.get(),
                lambda: has_flipped.set(lambda _: predicate(item)),
            ),
            (back if has_flipped.get() else front).append(item),
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

    export(__name__, Request),

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

        Request(method, path, headers, message_body),
    ]),

    export(__name__, parse)
])
