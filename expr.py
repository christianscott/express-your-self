import collections
import sys
import importlib

if not (sys.version_info[0] >= 3 and sys.version_info[1] >= 8):
    raise Exception("must be using at least python 3.8")

consume = lambda iterable: collections.deque(iterable, maxlen=0)

func = lambda bound_variables, body: body(**bound_variables)
λ = func

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
