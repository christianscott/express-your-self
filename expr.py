import collections

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

do = lambda *args: len(args) > 0 and last(args)

loop = lambda fn: consume(fn() for _ in iter(int, 1))

loop_while_true = lambda fn: fn() and loop(fn)()
