import collections

consume = lambda iterable: collections.deque(iterable, maxlen=0)

func = lambda body, bound_variables: body(**bound_variables)

where = lambda **kwargs: kwargs

last = lambda iterable: func(
    lambda array: \
        array[len(array) - 1],
    where(
        array=[*iterable]
    )
)

do = lambda *args: len(args) > 0 and last(args)

loop = lambda fn: consume(fn() for _ in iter(int, 1))

loop_while_true = lambda fn: fn() and loop(fn)()
