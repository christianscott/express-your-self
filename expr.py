import collections
import enum
import sys
import importlib


throw = lambda message, constructor = Exception: (_ for _ in ()).throw(constructor(message))

if_then = lambda predicate, action: predicate and action()

if_then(
    not sys.version_info[0] >= 3 and sys.version_info[1] >= 8,
    lambda: throw("must be using at least python 3.8. expr requires assignment expressions (e.g. x := 1), which were introduced in 3.8")
)

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

klass = lambda name, attrs: type(name, (), attrs)

Box = klass('Box', {
    '__init__': lambda self, value: setattr(self, 'value', value),
    'get': lambda self: self.value,
    'set': lambda self, setter: setattr(self, 'value', setter(self.value)),
})

consume = lambda iterable: collections.deque(iterable, maxlen=0)

loop = lambda fn: consume(fn() for _ in iter(int, 1))

Consumable = klass('Consumable', {
    "__init__": lambda self, fn: setattr(self, 'fn', fn),
    "__next__": lambda self: self.fn(),
    "__call__": lambda self: self.fn(),
})

loop_while = lambda fn: do([
    consumable := Consumable(fn),
    consume(iter(consumable, False)),
])

for_each = lambda iterable, callback: consume(
    callback(entry) for entry in iterable
)

require = importlib.import_module

t = collections.namedtuple

export = lambda module_name, value: do([
    module := sys.modules[module_name],
    setattr(module, value.__name__, value)
])
