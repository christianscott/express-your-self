import collections
import enum
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

klass = lambda name, attrs: type(name, (), attrs)

Consumable = klass('Consumable', {
    "__init__": lambda self, fn: setattr(self, 'fn', fn),
    "__next__": lambda self: self.fn(),
    "__call__": lambda self: self.fn(),
})

Box = klass('Box', {
    '__init__': lambda self, value: setattr(self, 'value', value),
    'get': lambda self: self.value,
    'set': lambda self, setter: setattr(self, 'value', setter(self.value)),
})

loop_while = lambda fn: do([
    consumable := Consumable(fn),
    consume(iter(consumable, False)),
])

require = importlib.import_module

t = collections.namedtuple

export = lambda module_name, value: do([
    module := sys.modules[module_name],
    setattr(module, value.__name__, value)
])
