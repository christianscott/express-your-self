import math

from expr import *

is_prime = lambda n: do([
    False if n <= 1 else \
    True  if n <= 3 else \
    False if n % 2 == 0 else \
    do([
        possible_divisors := range(3, math.floor(n / 2) + 1),
        has_divisors := any(n % m == 0 for m in possible_divisors),
        not has_divisors
    ])
])

consume(
    print(f"{i}: {is_prime(i)}") for i in range(30)
)
