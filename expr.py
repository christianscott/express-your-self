import collections
import sys
import importlib


throw = lambda message, constructor = Exception: (_ for _ in ()).throw(constructor(message))

if_then = lambda predicate, action: predicate and action()

if_then(
    not sys.version_info[0] >= 3 and sys.version_info[1] >= 8,
    lambda: throw("must be using at least python 3.8")
)

consume = lambda iterable: collections.deque(iterable, maxlen=0)

func = lambda bound_variables, body: body(**bound_variables)

let = lambda **kwargs: kwargs

last = lambda iterable: func(
    let(
        array=[*iterable]
    ),
    lambda array: \
        array[len(array) - 1],
)

do = lambda statements: len(statements) > 0 and last(statements)

loop = lambda fn: consume(fn() for _ in iter(int, 1))

loop_while_true = lambda fn: fn() and loop(fn)()

require = importlib.import_module
