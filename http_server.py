from expr import *

do([
    socket := require('socket'),
    threading := require('threading'),
    http := require('http'),

    fprint := lambda *args: do([
        print(*args, flush=True),
    ]),

    spawn := lambda target, args: do([
        handler_thread := threading.Thread(target=target, args=args),
        setattr(handler_thread, 'daemon', True),
        handler_thread.start()
    ]),

    CHUNK_SIZE := 1024,

    handle_client := lambda current_connection, client_addr: do([
        bytes_ := bytearray(),
        loop_while(lambda: do([
            chunk := current_connection.recv(1024),
            bytes_.extend(chunk),
            len(chunk) == CHUNK_SIZE,
        ])),
        message := bytes_.decode('utf8'),
        print(http.parse(message)),
        current_connection.send(b"HTTP/1.1 200 OK\r\n"),
    ]),

    listen := lambda host, port: do([
        connection := socket.socket(socket.AF_INET, socket.SOCK_STREAM),
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
        connection.bind((host, port)),

        # Listen for clients (max 10 clients in waiting)
        connection.listen(10),

        print(f"server listening on {host}:{port}"),

        loop(lambda: do([
            client_connection := connection.accept(),
            spawn(target=handle_client, args=client_connection),
        ]))
    ]),

    listen("localhost", 3000),
])
