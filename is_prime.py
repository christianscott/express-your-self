import math

from expr import *

has_divisors = lambda n: λ(
    let(
        possible_divisors=range(3, math.floor(n / 2) + 1)
    ),
    lambda possible_divisors: \
        any(n % m == 0 for m in possible_divisors)
)

is_prime = lambda n: \
    False if n <= 1 else \
    True  if n <= 3 else \
    False if n % 2 == 0 else \
    not has_divisors(n)

consume(
    print(f"{i}: {is_prime(i)}") for i in range(30)
)
