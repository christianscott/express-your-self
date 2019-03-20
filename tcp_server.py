import socket
import threading

from expr import *

spawn = lambda target, args: λ(
    let(
        handler_thread = threading.Thread(target=target, args=args)
    ),
    lambda handler_thread: do(
        setattr(handler_thread, 'daemon', True),
        handler_thread.start()
    )
)


handle_client = lambda current_connection, client_addr: \
    loop(lambda: do(
        # TODO: read until newline
        current_connection.send(current_connection.recv(1024))
    ))


listen = lambda host, port: λ(
    let(
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM),
    ),
    lambda connection: do(
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
        connection.bind((host, port)),
        # Listen for clients (max 10 clients in waiting)
        connection.listen(10),
        loop(lambda: λ(
            let(
                client_connection = connection.accept(),
            ),
            lambda client_connection: spawn(target=handle_client, args=client_connection),
        ))
    ),
)


listen("localhost", 3000)
