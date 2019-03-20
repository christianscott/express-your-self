import socket
import threading

from expr import *

spawn = lambda target, args: func(
    lambda handler_thread: do(
        setattr(handler_thread, 'daemon', True),
        handler_thread.start()
    ),
    where(
        handler_thread=threading.Thread(target=target, args=args)
    )
)

handle_client = lambda current_connection, client_addr: \
    loop(lambda: do(
        # TODO: read until newline
        current_connection.send(current_connection.recv(1024))
    ))


listen = lambda host, port: func(
    lambda connection: do(
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1),
        connection.bind((host, port)),
        # Listen for clients (max 10 clients in waiting)
        connection.listen(10),
        loop(lambda: func(
            lambda client_connection: spawn(target=handle_client, args=client_connection),
            where(
                client_connection=connection.accept(),
            )
        ))
    ),
    where(
        connection=socket.socket(socket.AF_INET, socket.SOCK_STREAM),
    )
)

listen("localhost", 3000)
