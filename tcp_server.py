import socket
import threading

from expr import *

spawn = lambda target, args: do([
    handler_thread := threading.Thread(target=target, args=args),
    setattr(handler_thread, 'daemon', True),
    handler_thread.start()
])


handle_client = lambda current_connection, client_addr: \
    loop(lambda: do([
        # TODO: read until newline
        current_connection.send(current_connection.recv(1024))
    ]))


listen = lambda host, port: do([
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
])


listen("localhost", 3000)
