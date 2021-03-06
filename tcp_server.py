from expr import *

do([
    socket := require('socket'),
    threading := require('threading'),

    spawn := lambda target, args: do([
        handler_thread := threading.Thread(target=target, args=args),
        setattr(handler_thread, 'daemon', True),
        handler_thread.start()
    ]),

    ends_with_newline := lambda bytes_: \
        len(bytes_) > 0 and bytes_[len(bytes_) - 1] == ord('\n'),

    handle_client := lambda current_connection, client_addr: do([
        print(f"client connected at {client_addr}"),
        loop_while(lambda: do([
            recvd_bytes := current_connection.recv(1024),
            current_connection.send(recvd_bytes),

            not ends_with_newline(recvd_bytes),
        ])),
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


    listen("localhost", 3000)
])
