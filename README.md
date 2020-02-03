# express-your-self

Python, with no statements!

Inside `expr.py` you'll find some utility functions and classes that let you write programs without any statements (barring a single import at the top of the file...).

I've also written a (sort-of working) [TCP server](https://github.com/christianscott/express-your-self/blob/master/tcp_server.py) and an [HTTP server](https://github.com/christianscott/express-your-self/blob/master/http_server.py).

Here's an example of the code you might write. This function tells you whether or not the supplied number is prime. Looks a little like lisp to me.

```python
from expr import * # the last statement you'll ever need

# `do` lets you sequence your "statements"
do([
    # we use/abuse the walrus operator to get variables
    math := require('math'),

    is_prime := lambda n: do([
        False if n <= 1 else \
        True  if n <= 3 else \
        False if n % 2 == 0 else \
        do([
            possible_divisors := range(3, math.floor(n / 2) + 1),
            has_divisors := any(n % m == 0 for m in possible_divisors),
            not has_divisors
        ])
    ]),

    consume(
        print(f"{i}: {is_prime(i)}") for i in range(30)
    )
])
```
