# express-your-self

Python, with no statements!

Inside `expr.py` you'll find some utility functions and classes that let you write programs without any statements (barring a single import at the top of the file...).

I've written a (sort-of working) [TCP server](https://github.com/christianscott/express-your-self/blob/master/tcp_server.py) and an [HTTP server](https://github.com/christianscott/express-your-self/blob/master/http_server.py).

Here's an example of the code you might write. This starts a mutli-threaded TCP server that simply echos whatever you send it. Try it out using `netcat`. (warning: it's a little broken)

```python
from expr import *

# `do` lets use sequence "statements"
do([
    # "walrus operator" gives us variables (python 3.8+)
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
        # loop_while calls the provided lambda over and over, until the final expression is falsy
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

```

The code in `http.py` and `http_server.py` is much more interesting. Cool things not included in this snippet:

- `t` is a way to get "data classes". You give it a name and a list of properties, as follows: `Pair := t('Pair', ['one', 'two'])`
- `Box` is to get around the fact that we don't have mutable bindings. Instead of the binding being mutable, just stick it in a container!
- `klass`, for when a data class isn't enough. Used to define `Box`:
```python
Box = klass('Box', {
    '__init__': lambda self, value: setattr(self, 'value', value),
    'get': lambda self: self.value,
    'set': lambda self, setter: setattr(self, 'value', setter(self.value)),
})
```

## improvements

- [ ] Exceptions! There's no way to catch exceptions at the moment. It would be easy to write a helper function using `try/catch` statements, but that's cheating.
